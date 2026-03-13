from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取上传的两个文件
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # 读取Excel文件
        df_current = pd.read_excel(file1)
        df_info = pd.read_excel(file2)
        
        # 匹配数据（使用left join保留所有当前数据行）
        merged = pd.merge(df_current, df_info, on='本企业代码', how='left')
        
        # 处理缺失值
        merged = merged.fillna({
            '成立时间': '未提供',
            '注册资本': '未提供',
            '持股比例': '未提供',
            '企业类别': '未提供',
            '主责主业范围': '未提供'
        })
        
        # 生成下载
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            merged.to_excel(writer, index=False)
        output.seek(0)
        
        return send_file(
            output, 
            download_name='匹配后的数据.xlsx', 
            as_attachment=True
        )
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
