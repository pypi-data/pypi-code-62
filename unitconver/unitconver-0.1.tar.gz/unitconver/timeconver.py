"""将天、小时、分钟任意一种单位的时间换算成其他单位时间,用于测试！"""


def time_conver(time):
    time_units = {'hour': ('h', 'hour', 'hours'),
                  'minute': ('m', 'min', 'minute', 'minutes'),
                  'day': ('d', 'day', 'days')}
    unit = ''.join([s for s in time if s.isalpha()])
    unit = unit.lower()
    num = ''.join([s for s in time if s.isdigit()])
    num = float(num)

    for key, value in time_units.items():
        if unit in value:
            if key == 'day':
                print(f'{num}{unit}是:\n\t{num*24}小时\n\t{num*24*60}分钟\n\t{num*24*60*60}秒')
            elif key == 'hour':
                print(f'{num}{unit}是:\n\t{num/24}天\n\t{num*60}分钟\n\t{num*60*60}秒')
            elif key == 'minute':
                print(f'{num}{unit}是:\n\t{num/60/24}天\n\t{num/60}小时\n\t{num*60}秒')
            break
        else:
            continue


if __name__ == '__main__':
    time_conver(input('请输入时间(仅支持天、小时、分钟任意一种单位)：'))