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

    function createStationMarker(pos) {
        markersArray.push(new google.maps.Marker({
            position: pos,
            map: map,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 5,
                fillOpacity: 1,
                fillColor: '#FF0000',
                strokeColor: '#FF0000'
            }
        }));
    }

    var model = {
        data: null,
        loadData: function() {
            $.ajax('/backend/' + cityId).done(function(data) {
                model.data = data;


                for (var i in data.lines) {
                    var line = data.lines[i];
                    for (var j in line.stations) {
                        var station = line.stations[j];
                        var myLatLng = new google.maps.LatLng(station.lat, station.lng);
                        createStationMarker(myLatLng);
                    }
                }
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

            var lines = form.find('#lines');
            lines.html('');

            _.each(model.data.lines, function(l) {
               lines.append($('<option>'), { value: l.id });
            });

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
/*            "edit": {name: "Edit", icon: "edit"},
            "delete": {name: "Delete", icon: "delete"}*/
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