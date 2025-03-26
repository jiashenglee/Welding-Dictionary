// 网页文件/app.js

// 修改API地址（替换YOUR_RENDER_APP_NAME为你的Render应用名）
const API_URL = 'https://welding-dictionary.onrender.com/api/search';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    // 绑定搜索按钮事件
    document.getElementById('searchButton').addEventListener('click', performSearch);
    
    // 其他初始化代码...
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
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                keywords: keywords.split(',').map(k => k.trim()),
                fuzzy: fuzzy
            })
        });

        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }

        resultsBody.innerHTML = '';
        data.results.forEach((item, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${item.term}</td>
                <td>${item.explanation}</td>
            `;
            resultsBody.appendChild(row);
        });

        resultStats.textContent = `找到 ${data.results.length} 条结果`;
        
    } catch (error) {
        console.error('搜索出错:', error);
        alert('搜索服务暂时不可用');
    }
}
