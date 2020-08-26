def number_to_human_size(B, precision=2):
    try:
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2)  # 1,048,576
        GB = float(KB ** 3)  # 1,073,741,824
        TB = float(KB ** 4)  # 1,099,511,627,776
        PB = float(KB ** 5)  # 1,125,899,906,842,624
    except ValueError:
        raise ValueError('Argument in number_to_human_size function must be numeric!')

    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{} KB'.format(round((B / KB), precision))
    elif MB <= B < GB:
        return '{} MB'.format(round((B / MB), precision))
    elif GB <= B < TB:
        return '{} GB'.format(round((B / GB), precision))
    elif TB <= B < PB:
        return '{} TB'.format(round((B / TB), precision))
    elif PB <= B:
        return '{} PB'.format(round((B / PB), precision))