# 服务器代码/app.py
from flask import Flask, jsonify, request
import os
from pathlib import Path
from flask_cors import CORS  # 新增：解决跨域问题

app = Flask(__name__)
CORS(app)  # 新增：允许所有域名访问

# 修改数据路径（自动适应Render环境）
DATA_DIR = Path(__file__).parent / "data"

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
                        "source": file_path.name
                    })
                    index += 1
    return results

# @app.route('/api/search', methods=['POST'])


# @app.route('/api/search', methods=['GET', 'POST'])  # 允许两种方法
# def handle_search():
#     # 根据请求方法获取参数
#     if request.method == 'POST':
#         data = request.get_json()
#         keywords = data.get('keywords', [])
#         fuzzy = data.get('fuzzy', False)
#     else:  # GET方法
#         keywords = request.args.get('keywords', '').split(',')
#         fuzzy = request.args.get('fuzzy', 'false').lower() == 'true'
     
#     if not keywords:
#         return jsonify({"error": "请输入搜索关键词"}), 400
    
#     results = search_files(keywords, fuzzy)
#     return jsonify({"results": results})

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
    
    return jsonify({"results": results})



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # 优先使用Render分配的端口
    app.run(host='0.0.0.0', port=port)  # 必须设置host为0.0.0.0
