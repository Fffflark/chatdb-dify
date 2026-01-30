import pandas as pd


def concat_tables(origin_path: str = './人员表（伪造.xlsx', expand_path: str ='./门禁表（伪造.xlsx') -> pd.DataFrame:
    table_expand = pd.read_excel(origin_path, header=1)   # 人员扩展信息表
    table_origin = pd.read_excel(expand_path, header=1)    # 门禁组人员表
    out_table = pd.DataFrame()

    # 序号列（从1开始）
    out_table['序号'] = range(1, len(table_origin) + 1)
    out_table['序号'] = out_table['序号'].astype(str)

    # 使用门禁表中的数据
    out_table['卡编号（印刷在卡上的数字串）'] = table_origin['人员编号'].astype(str)
    out_table['姓名'] = table_origin['姓名'].astype(str).str.replace(' ', '', regex=False)
    out_table['岗位类别编号'] = table_origin['部门编号'].astype(str)
    out_table['通行规则'] = table_origin['权限组名称'].astype(str)

    # 固定值字段
    out_table['是否激活'] = '是'

    # 生成证件照文件名
    out_table['2寸证件照（白底）'] = out_table['卡编号（印刷在卡上的数字串）'] + '.jpg'

    # 从扩展表合并其他字段
    out_table = out_table.merge(
        table_expand[['人员编号', '卡号', '地址', '性别', '部门名称', '职务', '身份证号', '手机']],
        left_on='卡编号（印刷在卡上的数字串）',
        right_on='人员编号',
        how='left'
    )
    # 重命名字段
    out_table = out_table.rename(columns={
        '卡号': 'RFID卡号',
        '地址': '二维码信息',
        '部门名称': '岗位类别',
        '手机': '联系方式'
    })
    # 处理证件类型字段
    out_table['证件类型'] = ''
    mask = out_table['身份证号'].notna() & (out_table['身份证号'].astype(str).str.strip() != '')
    out_table.loc[mask, '证件类型'] = '居民身份证'

    # 添加空白字段
    out_table['单位名称'] = ''
    out_table['备注'] = ''

    # 确保所有列都是str
    for col in out_table.columns:
        out_table[col] = out_table[col].astype(str)

    # 重新排列列顺序
    column_order = [
        '序号',
        '卡编号（印刷在卡上的数字串）',
        'RFID卡号',
        '二维码信息',
        '姓名',
        '性别',
        '岗位类别编号',
        '岗位类别',
        '单位名称',
        '职务',
        '身份证号',
        '2寸证件照（白底）',
        '联系方式',
        '证件类型',
        '通行规则',
        '是否激活',
        '备注'
    ]

    out_table = out_table[column_order]

    # 保存到Excel
    out_table.to_excel('out_table.xlsx', index=False)

    print(f"合并完成！共处理 {len(out_table)} 条记录")
    print(f"原表长度：{len(table_origin)}，最终表长度：{len(out_table)}")
    
    return out_table



    