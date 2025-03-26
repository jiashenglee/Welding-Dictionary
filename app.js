// 全局常量定义（必须放在最顶部）
const API_URL = 'https://welding-dictionary.onrender.com/api/search';

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('searchButton').addEventListener('click', performSearch);
});

async function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const fuzzyCheckbox = document.getElementById('fuzzySearch');
    const resultsBody = document.getElementById('resultsBody');
    const resultStats = document.getElementById('resultStats');
    
    const keywords = searchInput.value.trim();
    const fuzzy = fuzzyCheckbox.checked;

    if (!keywords) {
        alert('请输入搜索关键词');
        return;
    }

    try {
        // 关键修改：使用API_URL常量
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                keywords: keywords.split(/[,，]/), // 支持中英文逗号
                fuzzy: fuzzy
            })
        });

        // 增强响应处理
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP错误: ${response.status}`);
        }

        const data = await response.json();
        
        resultsBody.innerHTML = '';
        if (data.results.length === 0) {
            resultsBody.innerHTML = '<tr><td colspan="3">未找到匹配结果</td></tr>';
        } else {
            data.results.forEach((item, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${item.term}</td>
                    <td>${item.explanation}</td>
                `;
                resultsBody.appendChild(row);
            });
        }

        resultStats.textContent = `找到 ${data.results.length} 条结果`;
        
    } catch (error) {
        console.error('完整错误:', error);
        resultsBody.innerHTML = `<tr><td colspan="3" style="color:red">错误: ${error.message}</td></tr>`;
    }
}
