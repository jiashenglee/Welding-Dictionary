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

@app.route('/api/search', methods=['POST'])
def handle_search():
    data = request.json
    keywords = data.get('keywords', [])
    fuzzy = data.get('fuzzy', False)
    
    if not keywords:
        return jsonify({"error": "请输入搜索关键词"}), 400
    
    results = search_files(keywords, fuzzy)
    return jsonify({"results": results})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # 优先使用Render分配的端口
    app.run(host='0.0.0.0', port=port)  # 必须设置host为0.0.0.0
