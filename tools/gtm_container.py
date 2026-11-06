#!/usr/bin/env python3
"""Gera docs/gtm-container-eventos.json: contêiner do GTM para IMPORTAR (Admin > Importar contêiner > Mesclar).
Cria variáveis de camada de dados, 1 acionador de evento personalizado e 1 tag de evento do GA4 que repassa
todos os eventos do site ao GA4. Uso: python3 tools/gtm_container.py"""
import json, os, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
site = json.load(open(os.path.join(ROOT, 'data', 'site.json'), encoding='utf8'))
GTM_ID = site['gtm_id']
MEASUREMENT_ID = 'G-JF46WCSXS2'  # fluxo de dados do GA4 (confirme em Admin > Fluxos de dados)

EVENTS = ['hero_cta_click', 'nav_click', 'menu_toggle', 'section_nav_click', 'filter_select', 'product_click', 'book_click',
          'mentoring_click', 'project_click', 'featured_click', 'social_click', 'contact_click', 'newsletter_submit',
          'reco_expand', 'faq_toggle', 'carousel_scroll', 'scroll_depth', 'section_view', 'outbound_click', 'page_not_found']
PARAMS = ['page_path', 'section_id', 'placement', 'link_text', 'link_url', 'link_domain', 'book_id', 'store', 'category',
          'project_id', 'item_id', 'network', 'method', 'cta_id', 'filter', 'target', 'state', 'question', 'depth', 'missing_path']

A, C = '0', '0'
base = {'accountId': A, 'containerId': C}
variables = [dict(base, variableId=str(i + 1), name=f'DLV - {p}', type='v', notes=f'Parâmetro "{p}" empilhado pelo site no dataLayer.',
                  parameter=[{'type': 'INTEGER', 'key': 'dataLayerVersion', 'value': '2'},
                             {'type': 'BOOLEAN', 'key': 'setDefaultValue', 'value': 'false'},
                             {'type': 'TEMPLATE', 'key': 'name', 'value': p}]) for i, p in enumerate(PARAMS)]
trigger = dict(base, triggerId='1', name='CE - Eventos do site', type='CUSTOM_EVENT',
               customEventFilter=[{'type': 'MATCH_REGEX', 'parameter': [{'type': 'TEMPLATE', 'key': 'arg0', 'value': '{{_event}}'},
                                                                       {'type': 'TEMPLATE', 'key': 'arg1', 'value': '^(' + '|'.join(EVENTS) + ')$'}]}])
tag = dict(base, tagId='1', name='GA4 - Eventos do site', type='gaawe', firingTriggerId=['1'], tagFiringOption='ONCE_PER_EVENT',
           notes='Envia ao GA4 todo evento do site (nome = evento do dataLayer) com os parâmetros mapeados.',
           parameter=[{'type': 'BOOLEAN', 'key': 'sendEcommerceData', 'value': 'false'},
                      {'type': 'TEMPLATE', 'key': 'eventName', 'value': '{{Event}}'},
                      {'type': 'LIST', 'key': 'eventSettingsTable', 'list': [
                          {'type': 'MAP', 'map': [{'type': 'TEMPLATE', 'key': 'parameter', 'value': p},
                                                  {'type': 'TEMPLATE', 'key': 'parameterValue', 'value': '{{DLV - %s}}' % p}]} for p in PARAMS]},
                      {'type': 'TEMPLATE', 'key': 'measurementIdOverride', 'value': MEASUREMENT_ID}])
out = {'exportFormatVersion': 2, 'exportTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
       'containerVersion': {'path': 'accounts/0/containers/0/versions/0', 'accountId': A, 'containerId': C, 'containerVersionId': '0',
                            'container': dict(base, name='pauloleite.dev', publicId=GTM_ID, usageContext=['WEB']),
                            'tag': [tag], 'trigger': [trigger], 'variable': variables,
                            'builtInVariable': [dict(base, type='EVENT', name='Event')]}}
path = os.path.join(ROOT, 'docs', 'gtm-container-eventos.json')
open(path, 'w', encoding='utf8').write(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print('Gerado:', path, '|', len(EVENTS), 'eventos,', len(PARAMS), 'parâmetros')
