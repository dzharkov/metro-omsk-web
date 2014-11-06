$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$(document).ready(function() {
    var overlayItems = [];
    var map;

    google.maps.Map.prototype.clearOverlays = function() {
          for (var i = 0; i < overlayItems.length; i++ ) {
            overlayItems[i].setMap(null);
          }
          overlayItems.length = 0;
    };

    function createStationMarker(pos, color, station) {
        overlayItems.push(new MarkerWithLabel({
            position: pos,
            map: map,
            labelContent: station.name,
            draggable:true,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 3,
                fillOpacity: 1,
                fillColor: color,
                strokeColor: color
            }
        }));

        return overlayItems[overlayItems.length - 1];
    }

    var model = {
        data: null,
        lineById: function(id) {
            return _.find(this.data.lines, function(l) {return l.id == id;});
        },
        loadData: function() {
            $.ajax('/backend/' + cityId).done(function(data) {
                map.clearOverlays();
                model.data = data;

                _.each(data.lines, function(line) {
                    var lineArray = [];
                    var linePath;
                    _.each(line.stations, function(station) {
                        station.line_id = line.id;
                        var myLatLng = new google.maps.LatLng(station.lat, station.lng);
                        var marker = createStationMarker(myLatLng, line.color, station);
                        google.maps.event.addListener(marker, 'rightclick', function(mouseEvent) {
                            model.currentStation = station;
                            $('.context-menu-marker').contextMenu(mouseEvent.pixel);
                        });

                        google.maps.event.addListener(marker, 'dragend', function(mouseEvent) {
                            var data = {
                                ln: mouseEvent.latLng.B,
                                lt: mouseEvent.latLng.k
                            };
                            $.post('/backend/update_coords/' + station.id, data).done(
                                function () {
                                    model.loadData();
                                }
                            );
                        });

                        lineArray.push(myLatLng);
                    });
                    linePath = new google.maps.Polyline({
                        path: lineArray,
                        geodesic: true,
                        strokeColor: line.color,
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                    });
                    overlayItems.push(linePath);
                    linePath.setMap(map);
                });
            });
        },
        openStationForm: function(station) {
            station = station || {};
            var modalDiv = $('#create-station-modal');
            modalDiv.modal({show:true});

            var form = modalDiv.find('form');
            form.find('.js-cancel').click(function() { modalDiv.modal('hide'); });
            form.find('#name').val( station.name || '');
            form.find('#next_time').val( station.next_time || '');

            var lines = form.find('#line');
            lines.html('');

            var stations = form.find('#next_id');

            function filterStations() {
                var lineId = lines.find('option:selected').attr('value');
                stations.html('');
                var line = model.lineById(lineId);

                stations.append($('<option>', { value: '', text: 'Добавить последней' }));
                _.each(line.stations, function(s) {
                    var desc = { value: s.id, text: s.name };
                    if (station.next_station_id == s.id) {
                        desc.selected = "selected";
                    }
                    stations.append($('<option>', desc));
                });
            }

            lines.change(filterStations);
            var lineId = station.line_id || -1;
            _.each(model.data.lines, function(l) {
                var desc = { value: l.id, text: l.name };
                if (l.id == lineId) {
                    desc.selected = "selected";
                }
                lines.append($('<option>', desc));
            });

            filterStations();

            form.unbind('submit');
            form.submit(function(event) {
                var data = $(this).serializeObject();

                data.ln = station.lng || model.createLatLng.B;
                data.lt = station.lat || model.createLatLng.k;

                var url = '/backend/add_station';
                if (station.id) {
                    url = '/backend/edit_station/' + station.id;
                }

                $.post(url, data).done(function() {
                    modalDiv.modal('hide');
                    model.loadData();
                });
                return false;
            });
        },
        createLatLng: null
    };

    $.contextMenu({
        selector: '.context-menu-1',
        trigger: 'none',
        callback: function(key, options) {
            model.openStationForm();
        },
        items: {
            "add": {name: "Add station", icon: "add"}
        }
    });

    $.contextMenu({
        selector: '.context-menu-marker',
        trigger: 'none',
        callback: function(key, options) {
            model.openStationForm(model.currentStation)
        },
        items: {
            "edit": {name: "Edit", icon: "edit"}
        }
    });

    var cityId = $('#city-id').attr('value');
    var cityLn = $('#city-ln').attr('value');
    var cityLt = $('#city-lt').attr('value');

    function initializeMap() {
        var mapOptions = {
            zoom: 10,
            center: new google.maps.LatLng(cityLt, cityLn),
            styles: [
                {
                    featureType: "transit",
                    stylers: [
                        { visibility: "off" }
                    ]
                }
            ]
        };
        map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

        model.loadData();

        google.maps.event.addListener(map, 'rightclick', function(mouseEvent){
            $('.context-menu-1').contextMenu(mouseEvent.pixel);
            model.createLatLng = mouseEvent.latLng;
            map.setOptions({ draggableCursor: 'pointer' });
        });
    }

    google.maps.event.addDomListener(window, 'load', initializeMap);
});