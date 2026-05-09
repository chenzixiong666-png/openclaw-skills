import zipfile
import xml.etree.ElementTree as ET

file_path = r"C:\Users\woan\.openclaw\media\inbound\测试长运指标用例---bf3c320e-3746-4dba-97dc-550086c3149c.xlsx"

# 打开 Excel 文件（本质上是 zip）
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    # 读取 sharedStrings.xml（包含所有字符串）
    with zip_ref.open('xl/sharedStrings.xml') as f:
        strings_xml = f.read().decode('utf-8')
        root = ET.fromstring(strings_xml)
        
        print("字符串列表（前100个）:")
        print("="*120)
        ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        
        for idx, si in enumerate(root.findall('.//main:si', ns)[:100]):
            text_elem = si.find('main:t', ns)
            if text_elem is not None:
                print(f"{idx}: {text_elem.text}")
        print("="*120)
