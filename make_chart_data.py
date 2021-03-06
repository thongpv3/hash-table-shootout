# random,1310720,google_dense_hash_map,45621248,0.344362020493
# random,2621440,glib_hash_table,109867008,1.01163601875
# random,2621440,stl_unordered_map,130715648,1.73484396935
# random,2621440,boost_unordered_map,108380160,1.11585187912
# random,2621440,google_sparse_hash_map,37015552,1.76031804085
# random,2621440,google_dense_hash_map,79175680,0.504401922226
# random,5242880,glib_hash_table,210530304,1.86031603813
# random,5242880,stl_unordered_map,250298368,3.81597208977
# random,5242880,boost_unordered_map,192184320,2.63760495186
# random,5242880,google_sparse_hash_map,62066688,3.93570995331
# random,5242880,google_dense_hash_map,146284544,1.22620105743
# random,10485760,glib_hash_table,411856896,4.16937494278
# random,10485760,stl_unordered_map,490430464,7.91806197166
# random,10485760,boost_unordered_map,359251968,7.52085900307
# random,10485760,google_sparse_hash_map,111902720,8.11318516731
# random,10485760,google_dense_hash_map,280502272,2.32930994034
# random,20971520,glib_hash_table,814510080,8.32456207275
# random,20971520,stl_unordered_map,971583488,16.1606841087
# random,20971520,boost_unordered_map,692441088,24.5845990181
# random,20971520,google_sparse_hash_map,211435520,16.2772600651
# random,20971520,google_dense_hash_map,548937728,4.85360789299
# random,41943040,glib_hash_table,1619816448,90.6313672066

import sys, json

lines = [ line.strip() for line in sys.stdin if line.strip() ]

by_benchtype = {}

for line in lines:
    benchtype, nkeys, program, nbytes, runtime = line.split(',')
    nkeys = int(nkeys)
    nbytes = int(nbytes)
    runtime = float(runtime)

    by_benchtype.setdefault("%s-runtime" % benchtype, {}).setdefault(program, []).append([nkeys, runtime])
    if benchtype in ('randomfull', 'insertstring', 'insertsmallstring'):
        by_benchtype.setdefault("%s-memory"  % benchtype, {}).setdefault(program, []).append([nkeys, nbytes])

proper_names = {
    'boost_unordered_map': 'Boost 1.61 unordered_map',
    'stl_unordered_map': 'GCC 6.1 std::unordered_map',
    'google_sparse_hash_map': 'Google sparsehash 2.0.2 sparse_hash_map',
    'google_dense_hash_map': 'Google sparsehash 2.0.2 dense_hash_map',
    'qt_qhash': 'Qt 4.8 QHash',
    'hopscotch_map': 'Hopscotch map 0.4.1 with H=62',
    'spp_sparse_hash_map': 'Sparse hash map',
    'sherwood_map': 'Sherwood map',
    'emilib_hash_map': 'Emilib hash map',
    'rabbit_unordered_map': 'Rabbit unordered map',
    'rabbit_sparse_unordered_map': 'Rabbit sparse unordered map',
}

# do them in the desired order to make the legend not overlap the chart data
# too much
program_slugs = [
    'google_sparse_hash_map',
    'google_dense_hash_map',
    'stl_unordered_map',
    'boost_unordered_map',
    'qt_qhash',
    'hopscotch_map',
    'spp_sparse_hash_map',
    'sherwood_map',
    'emilib_hash_map',
    'rabbit_unordered_map',
    'rabbit_sparse_unordered_map',
]

chart_data = {}

for i, (benchtype, programs) in enumerate(by_benchtype.items()):
    chart_data[benchtype] = []
    for j, program in enumerate(program_slugs):
        data = programs[program]
        chart_data[benchtype].append({
            'label': proper_names[program],
            'data': [],
        })

        for k, (nkeys, value) in enumerate(data):
            chart_data[benchtype][-1]['data'].append([nkeys, value])

json_text = json.dumps(chart_data)
json_text = json_text.replace("}], ", "}], \n")
print('chart_data = ' + json_text)
