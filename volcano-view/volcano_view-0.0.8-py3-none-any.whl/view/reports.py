import codecs

from datetime import datetime

from .web_exc import WebException
from .my_tools import read_json_wx
from .the_time import IvlDef
from .my_tools import deserialize_tstamp, to_map


def build_report(reader, env, log) -> int:
    try:
        reader.reload_wx()
        report_cfg = read_json_wx(env.report)

        try:
            rep_name = report_cfg['name']
            rep_path = report_cfg['path']
            hr_ids = report_cfg['hrs']
            qt_id = report_cfg['qt']
            all_ivl_s = report_cfg['all_ivl']
            sub_ivl_s = report_cfg['sub_ivl']
            finished = report_cfg['finished']
            setpt_str = report_cfg['setpt']
        except KeyError as ex:
            raise WebException('File {} doesnt contain parameter {}'.format(env.report, ex))
            
        try: 
            all_ivl = IvlDef.parse ( all_ivl_s )
            sub_ivl = IvlDef.parse ( sub_ivl_s )
            
            setpt = None
            if setpt_str:
                setpt = deserialize_tstamp(setpt_str)   # *ValueError
                
        except ValueError as ex: 
            raise WebException(ex)

        hr_info = reader.read_hr_wx('cumulative')
        report_data = reader.read_data_wx (hr_ids, qt_id, all_ivl, sub_ivl, finished, setpt, dtm_to_str=False)
        
        dtm = datetime.now()
        report_file_name = '{}/{}_{}-{:02}-{:02} {:02}-{:02}'.format(rep_path or ".", rep_name, dtm.year, dtm.month, dtm.day, dtm.hour, dtm.minute)
        
        try:
            #with open(report_file_name + '.json', 'w') as f:
            #    f.write(json.dumps(report_data, indent=2))

            with codecs.open(report_file_name + '.html', 'w', encoding='utf-8') as f:
                _flush_report(hr_info, report_data, f, report_cfg, log)
                
            log.info('Successfully saved report {}'.format(report_file_name))
            
        except Exception as ex:
            raise WebException('Error saving report {}: {}'.format(report_file_name, ex))
            

    except WebException as ex:
        log.error(ex)
        return 1

    return 0


def _flush_report(hr_info, report_data, f, cfg, _log):
    '''
        hr_info: ( {id, parent_id, title}, ... )
        
        report_data: {
            'cumulative': True, 
            'start': '2020-07-16T00:00:00', 
            'readouts': ('2020-07-16T01:00:00', ...), 
            'series': [
                {
                'hr_id': 'site1', 
                'qt_id': 'eap', 
                'values': (577, ...)
                }, 
                ...
            ]
        }
    '''
    hr_map = to_map(hr_info, 'id')
    series = report_data['series']
    readouts = report_data['readouts']
    hdr_tm_fmt = cfg['header_time_format']
    tm_fmt = cfg['readout_time_format']

    f.write('<html>')
    f.write('  <head>')
    css = cfg.get('css', None)
    if css:
        f.write('<link rel="stylesheet" href="{}">'.format(css))
    f.write('  </head>')
    f.write('  <body>')
    
    last = readouts[len(readouts) - 1]
    f.write('<h5>Отчетный период: {} - {}</h5>'.format(report_data["start"].strftime(hdr_tm_fmt), last.strftime(hdr_tm_fmt)))
    
    
    f.write('    <table class="table table-striped">')
    f.write('      <thead>')
    f.write('        <tr>')
    f.write('          <th>Время</th>')
    for s in series:
        hr_id = s['hr_id']
        hr = hr_map.get(hr_id, None)
        hr_title= hr['title'] if hr else hr_id
        f.write('<th>{}</th>'.format(hr_title))
    f.write('        </tr>')
    f.write('      </thead>')
    f.write('      <tbody>')
    
    for i, d in enumerate(readouts):
        # d1 = readouts[i-1] if i > 0 else report_data['start']
        # d2 = readouts[i]
        f.write('<tr>')
        # f.write(f'<td>{d1.strftime(tm_fmt)} .. {d2.strftime(tm_fmt)}</td>')
        f.write('<td>{}</td>'.format(d.strftime(tm_fmt)))
        for s in series:
            v = s['values'][i]
            # html += '<td>' + (v === null ? 'Н/Д' : Math.floor(v*100)/100) + '</td>';
            f.write('<td>{}</td>'.format("Н/Д" if v is None else v))
        f.write('</tr>')

    f.write('<tr>')
    '''
    f.write('<th>SUM</th>')
    for s in series:
        f.write(f'<th>{s}</th>')
    f.write('</tr>')
    '''
    
    f.write('      </tbody>')
    f.write('    </table>')
    f.write('  </body>')
    f.write('</html>')
    