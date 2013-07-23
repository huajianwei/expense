#encoding: utf-8

#local_config, should be ignored in repository

nr_items = 20 #每页条目数量

item_names = ['name', 'disp', 'readonly', 'enum', 'value']
fields = [
    ['gid',         '编号', True,   False, ''],
    ['time',        '时间', False,  False, ''],
    ['direction',   '类型', False,  ['支出', '收入'], ''],
    ['amount',      '金额', False,  False, ''],
    ['remain',      '余额', True,   False, ''],
    ['who',         '人员', False,  ['小A', '小B', '小C', '其他'], ''],
    ['reason',      '用途', False,  False, ''],
    ['remark',      '备注', False,  False, ''],
]

outcome = 0
income = 1

fields_conf = {}
enum_conf = {}

for item in fields:
    item = dict(zip(item_names, item))
    fields_conf[item['name']] = item

need_login = False
user_conf = {
    'root': '123456',
}
