# 服务器代码/app.py
from flask import Flask, jsonify, request
import os
from pathlib import Path
from flask_cors import CORS  # 新增：解决跨域问题
import re  # 新增：正则表达式支持

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 新增这行禁用ASCII编码
CORS(app)  # 新增：允许所有域名访问

# # 修改数据路径（自动适应Render环境）
# DATA_DIR = Path(__file__).parent / "data"

# 修改为绝对路径（Render专用）
import os
DATA_DIR = Path(os.path.dirname(__file__)) / "data"  # 使用os模块确保路径正确

# 添加路径验证
if not DATA_DIR.exists():
    raise Exception(f"数据目录不存在：{DATA_DIR}")



def search_files(keywords, fuzzy=False):
    results = []
    index = 1
    
    for file_path in DATA_DIR.glob("**/*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # 支持中英文冒号
                if ':' in line:
                    term, explanation = line.split(':', 1)
                elif '：' in line:
                    term, explanation = line.split('：', 1)
                else:
                    continue
                
                term = term.strip()
                explanation = explanation.strip()
                
                # 新增：提取图片标签
                image_tag = ""
                match = re.search(r'<(.*?)>', explanation)
                if match:
                    image_tag = match.group(1).strip()
                    explanation = re.sub(r'<.*?>', '', explanation).strip()

                # 匹配逻辑
                match = False
                for kw in keywords:
                    kw = kw.lower()
                    target = term.lower()
                    if fuzzy:
                        if kw in target:
                            match = True
                            break
                    else:
                        if kw == target:
                            match = True
                            break
                
                if match:
                    results.append({
                        "index": index,
                        "term": term,
                        "explanation": explanation,
                        "image": image_tag if image_tag != "无" else "",  # 新增图片字段
                        "source": file_path.name
                    })
                    index += 1
    return results

# 在文件末尾新增图片路由
from flask import send_from_directory  # 新增导入

@app.route('/images/<filename>')  # 新增路由
def serve_image(filename):
    return send_from_directory(DATA_DIR / 'pic', filename)

@app.route('/api/search', methods=['GET', 'POST'])
def handle_search():
    # 增强日志输出
    print("\n=== 收到搜索请求 ===")
    print(f"请求方法: {request.method}")
    
    if request.method == 'POST':
        data = request.get_json()
        keywords = data.get('keywords', [])
        fuzzy = data.get('fuzzy', False)
    else:
        keywords = request.args.get('keywords', '').split(',')
        fuzzy = request.args.get('fuzzy', 'false').lower() == 'true'
    
    # 打印参数详情
    print(f"原始关键词参数: {request.args.get('keywords', '')}")
    print(f"处理后的关键词列表: {keywords}")
    print(f"模糊搜索状态: {fuzzy}")
    
    # 参数验证日志
    if not keywords:
        print("!! 错误：未接收到有效关键词")
        return jsonify({"error": "请输入搜索关键词"}), 400
    
    # 打印数据目录信息
    print(f"\n数据目录路径: {DATA_DIR.resolve()}")
    print(f"找到的数据文件列表: {list(DATA_DIR.glob('**/*.txt'))}")
    
    # 执行搜索并记录过程
    print("\n开始搜索...")
    results = search_files(keywords, fuzzy)
    print(f"找到 {len(results)} 条结果")
    
    return jsonify({"results": results}), 200, {'Content-Type': 'application/json; charset=utf-8'}



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # 优先使用Render分配的端口
    app.run(host='0.0.0.0', port=port)  # 必须设置host为0.0.0.0
