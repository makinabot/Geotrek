var Geotrek = Geotrek || {};

Geotrek.TopologyHelper = (function() {

    /**
     * This static function takes a list of Dijkstra results, and returns
     * a serialized topology, as expected by form widget, as well as a 
     * multiline geometry for highlight the result.
     */
    function buildSubTopology(paths, polylines, ll_start, ll_end, offset) {
        var polyline_start = polylines[0]
          , polyline_end = polylines[polylines.length - 1]
          , single_path = paths.length == 1 || polyline_start == polyline_end
          , single_path_loop = false
          , positions = {};

        if (!polyline_start || !polyline_end) {
            console.error("Could not compute distances without polylines.");
            return null;  // TODO: clean-up before give-up ?
        }

        if (window.DEBUG) {
            console.log('Start on layer ' + polyline_start.properties.pk + ' ' + ll_start.toString());
            console.log('End on layer ' + polyline_end.properties.pk + ' ' + ll_end.toString());
        }

        var percentageDistance = L.GeomUtils.getPercentageDistanceFromPolyline;
        var start = percentageDistance(ll_start, polyline_start)
          , end = percentageDistance(ll_end, polyline_end);
        if (!start || !end) {
            console.error("Could not compute distances withing paths.");
            return null;  // TODO: clean-up before give-up ?
        }
        var closest_first_idx = start.closest
          , closest_end_idx = end.closest;

        var lls_tmp, lls_end, latlngs = [];

        if (single_path) {
            var path_pk = paths[0],
                lls = polyline_start.getLatLngs(),
                single_path_loop = lls[0].equals(lls[lls.length-1]);

            if (single_path_loop && Math.abs(end.distance - start.distance) > 0.5) {
                /*
                 *        A
                 *     //=|---+
                 *   +//      |   It is shorter to go through
                 *    \\      |   extremeties than the whole loop
                 *     \\=|---+
  i              *        B
                 */
                if (end.distance - start.distance > 0.5) {
                    paths = [path_pk, path_pk];
                    positions[0] = [start.distance, 0.0];
                    positions[1] = [1.0, end.distance];
                    lls_tmp = lls.slice(0, closest_first_idx+1);
                    lls_tmp.reverse();
                    lls_tmp.unshift(ll_start);
                    lls_tmp.push(lls[0]);
                    var _end = lls.slice(closest_end_idx+1);
                    _end.reverse();
                    lls_tmp = lls_tmp.concat(_end);
                    lls_tmp.push(ll_end);
                }
                else if (end.distance - start.distance < -0.5) {
                    paths = [path_pk, path_pk];
                    positions[0] = [end.distance, 0.0];
                    positions[1] = [1.0, start.distance];
                    lls_tmp = lls.slice(closest_first_idx+1);
                    lls_tmp.unshift(ll_start);
                    lls_tmp.push(lls[0]);
                    lls_tmp = lls_tmp.concat(lls.slice(0, closest_end_idx+1));
                    lls_tmp.push(ll_end);
                }
            }
            else {
                paths = paths.unique();
                positions[0] = [start.distance, end.distance];

                var _ll_end, _ll_start, _closest_first_idx, _closest_end_idx;
                if (closest_first_idx < closest_end_idx) {
                    /*        A     B 
                     *   +----|=====|---->
                     */
                    _ll_end = ll_end, _ll_start = ll_start;
                    _closest_first_idx = closest_first_idx, _closest_end_idx = closest_end_idx;
                } else {
                    /*        B     A 
                     *   +----|=====|---->
                     */
                    _ll_end = ll_start, _ll_start = ll_end;
                    _closest_first_idx = closest_end_idx, _closest_end_idx = closest_first_idx;
                }
                lls_tmp = lls.slice(_closest_first_idx+1, _closest_end_idx+1);
                lls_tmp.unshift(_ll_start);
                lls_tmp.push(_ll_end);
            }
            latlngs.push(lls_tmp);
        }
        else {
            /*
             * Add first portion of line
             */
            var polyline_next = polylines[1],
                start_bound_by_first_point = L.GeomUtils.isStartAtEdges(polyline_start, polyline_next);

            var start_lls = polyline_start.getLatLngs(),
                start_on_loop = start_lls[0].equals(start_lls[start_lls.length-1]);

            if (start_bound_by_first_point) {
                /*
                 *       A
                 *    /--|===+    B
                 *  +/       \\+==|---
                 *   \       /
                 *    \-----+
                 */
                if (start_on_loop && start.distance > 0.5) {
                    lls_tmp = polyline_start.getLatLngs().slice(closest_first_idx + 1);
                    lls_tmp.unshift(ll_start);
                    positions[0] = [start.distance, 1.0];
                }
                else {
                    /*
                     *        A               B
                     *   <----|------++-------|----
                     *
                     *   <----|=====|++=======|----
                     *
                     * first point is shared ; include closest
                     */
                    lls_tmp = polyline_start.getLatLngs().slice(0, closest_first_idx + 1);
                    lls_tmp.push(ll_start);
                    polylines[0] = L.GeomUtils.lineReverse(polyline_start);
                    positions[0] = [start.distance, 0.0];
                }
            } else {
                /*
                 *        A               B
                 *   +----|------>+-------|----
                 *
                 *   +----|=====|>+=======|----
                 *
                 * first point is not shared ; don't include closest
                 */
                lls_tmp = polyline_start.getLatLngs().slice(closest_first_idx + 1);
                lls_tmp.unshift(ll_start);
                positions[0] = [start.distance, 1.0];
            }

            latlngs.push(lls_tmp);

            /* 
             * Add all intermediary lines
             */
            for (var i=1; i<polylines.length-1; i++) {
                var previous = polylines[i-1],
                    polyline = polylines[i];
                if (!L.GeomUtils.isAfter(polyline, previous)) {
                    positions[i] = [1.0, 0.0];
                    polylines[i] = L.GeomUtils.lineReverse(polyline);
                }
                latlngs.push(polylines[i].getLatLngs());
            }

            /*
             * Add last portion of line
             */
            var end_bound_by_first_point = L.GeomUtils.isStartAtEdges(polyline_end, polylines[polylines.length - 2]);

            var end_lls = polyline_end.getLatLngs(),
                end_on_loop = end_lls[0].equals(end_lls[end_lls.length-1]);

            if (end_bound_by_first_point) {
                if (end_on_loop && end.distance > 0.5) {
                    /*
                     *              B
                     *     A    //==|-+
                     *  ---|==+//     |
                     *         \      |
                     *          \-----+
                     */
                    lls_tmp = polyline_end.getLatLngs().slice(closest_end_idx + 1);
                    lls_tmp.unshift(ll_end);
                    positions[polylines.length - 1] = [end.distance, 1.0];
                }
                else {
                    /*
                     *        A               B
                     *   -----|------++-------|---->
                     *
                     *   -----|======+|=======>---->
                     */
                     // first point is shared ; include closest
                    lls_tmp = polyline_end.getLatLngs().slice(0, closest_end_idx + 1);
                    lls_tmp.push(ll_end);
                    positions[polylines.length - 1] = [0.0, end.distance];
                }
            } else {
                /*
                 *        A               B
                 *   -----|------+<-------|----+
                 *
                 *   -----|=====|+<=======|----+
                 */
                // first point is not shared ; don't include closest
                lls_tmp = polyline_end.getLatLngs().slice(closest_end_idx + 1);
                lls_tmp.unshift(ll_end);
                positions[polylines.length - 1] = [1.0, end.distance];
            }

            latlngs.push(lls_tmp);
        }

        // Clean-up :
        // We basically remove all points where position is [x,x]
        // This can happen at extremity points...
        if (!single_path_loop) {
            var cleanpaths = [],
                cleanpositions = {};
            for (var i=0; i<paths.length; i++) {
                var path = paths[i];
                if (i in positions) {
                    if (positions[i][0] != positions[i][1] && cleanpaths.indexOf(path) == -1) {
                        cleanpaths.push(path);
                        cleanpositions[i] = positions[i];
                    }
                }
                else {
                    cleanpaths.push(path);
                }
            }
            paths = cleanpaths;
            positions = cleanpositions;
        }

        // Safety warning.
        if (paths.length == 0)
            console.error('Empty topology. Expect problems. (' + JSON.stringify({positions:positions, paths:paths}) + ')');

        return {
            topology: {
                offset: offset,       // Float for offset
                positions: positions, // Positions on paths
                paths: paths          // List of pks
            },
            multipolyline: L.multiPolyline(latlngs)
        };
    };


    function buildTopologyFromComputedPath(idToLayer, data) {
        /**
         * @param idToLayer : callback to obtain a layer object from a pk/id.
         * @data : computed_path
         */
        if (!data.computed_paths) {
            return {
                layer: null,
                serialized: null
            }
        }

        var computed_paths = data['computed_paths']
          , edges = data['new_edges']
          , offset = 0.0  // TODO: input for offset
          , data = []
          , layer = L.featureGroup();

        if (window.DEBUG) { console.log('----'); console.log('Topology has ' + computed_paths.length + ' sub-topologies.'); }

        for (var i = 0; i < computed_paths.length; i++ ) {
            var cpath = computed_paths[i]
              , paths = $.map(edges[i], function(edge) { return edge.id; })
              , polylines = $.map(edges[i], function(edge) { return idToLayer(edge.id); });

            var topo = buildSubTopology(paths,
                                        polylines, 
                                        cpath.from_pop.ll,
                                        cpath.to_pop.ll,
                                        offset);
            if (!topo) break;

            data.push(topo.topology);
            if (window.DEBUG) console.log('subtopo[' + i + '] : ' + JSON.stringify(topo.topology));

            // Multilines for each sub-topology
            var group_layer = topo.multipolyline;
            group_layer.from_pop = cpath.from_pop;
            group_layer.to_pop = cpath.to_pop;
            group_layer.step_idx = i;
            layer.addLayer(group_layer);
        }
        if (window.DEBUG) console.log('----');

        return {
            layer: layer,
            serialized: data
        };
    }

    return {
        buildTopologyGeom: buildSubTopology,
        buildTopologyFromComputedPath: buildTopologyFromComputedPath
    };
})();
