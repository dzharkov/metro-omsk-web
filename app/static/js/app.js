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
    var markersArray = [];
    var map;

    google.maps.Map.prototype.clearOverlays = function() {
          for (var i = 0; i < markersArray.length; i++ ) {
            markersArray[i].setMap(null);
          }
          markersArray.length = 0;
    };

    function createStationMarker(pos, color, station) {
        markersArray.push(new MarkerWithLabel({
            position: pos,
            map: map,
            labelContent: station.name,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 3,
                fillOpacity: 1,
                fillColor: color,
                strokeColor: color
            }
        }));
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
                    _.each(line.stations, function(station) {
                        var myLatLng = new google.maps.LatLng(station.lat, station.lng);
                        createStationMarker(myLatLng, line.color, station);
                        lineArray.push(myLatLng);
                    });
                    var linePath = new google.maps.Polyline({
                        path: lineArray,
                        geodesic: true,
                        strokeColor: line.color,
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                    });
                    linePath.setMap(map);
                });
            });
        },
        createLatLng: null
    };

    $.contextMenu({
        selector: '.context-menu-one',
        trigger: 'none',
        callback: function(key, options) {
            //dialog.dialog( "open" );
            var modalDiv = $('#create-station-modal');
            modalDiv.modal({show:true});

            var form = modalDiv.find('form');
            form.find('.js-cancel').click(function() { modalDiv.modal('hide'); });

            var lines = form.find('#line');
            lines.html('');

            var stations = form.find('#next_id');

            function filterStations() {
                var lineId = lines.find('option:selected').attr('value');
                stations.html('');
                var line = model.lineById(lineId);

                _.each(line.stations, function(s) {
                    stations.append($('<option>', { value: s.id, text: s.name }));
                });

                stations.append($('<option>', { value: '', text: 'Добавить последней' }));
            }

            lines.change(filterStations);

            _.each(model.data.lines, function(l) {
               lines.append($('<option>', { value: l.id, text: l.name }));
            });

            filterStations();

            form.unbind('submit');
            form.submit(function(event) {
                var data = $(this).serializeObject();

                data.lan = model.createLatLng.B;
                data.lat = model.createLatLng.k;

                $.post('/backend/add_station', data).done(function() {
                    modalDiv.modal('hide');
                    model.loadData();
                });
                return false;
            });
        },
        items: {
            "add": {name: "Add station", icon: "add"}
        }
    });

    var cityId = $('#city-id').attr('value');

    function initializeMap() {
        var mapOptions = {
            zoom: 10,
            center: new google.maps.LatLng(54.987864, 73.367354)
        };
        map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

        model.loadData();

        google.maps.event.addListener(map, 'rightclick', function(mouseEvent){
            $('.context-menu-one').contextMenu(mouseEvent.pixel);
            model.createLatLng = mouseEvent.latLng;
            map.setOptions({ draggableCursor: 'pointer' });
        });
    }

    google.maps.event.addDomListener(window, 'load', initializeMap);
});