// ==== app.js 完整修正版 ====
(function() {
    // 1. 全局常量定义（立即执行函数内部）
    const API_URL = 'https://welding-dictionary.onrender.com/api/search';
    
    // 2. 打印调试信息
    console.log('API服务地址:', API_URL);
    
    // 3. 页面初始化
    document.addEventListener('DOMContentLoaded', function() {
        // 4. 元素安全检查
        const searchButton = document.getElementById('searchButton');
        if (!searchButton) {
            console.error('搜索按钮未找到！');
            return;
        }
        
        // 5. 事件绑定
        searchButton.addEventListener('click', performSearch);
    });

    // 6. 搜索函数
    async function performSearch() {
        console.log('正在请求:', API_URL); // 调试点
        
        try {
            const response = await fetch(API_URL, { // 使用常量
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    keywords: document.getElementById('searchInput').value.trim().split(/[,，]/),
                    fuzzy: document.getElementById('fuzzySearch').checked
                })
            });
            
            // ...其余处理逻辑保持不变...
        } catch (error) {
            console.error('完整错误:', error);
        }
    }
})(); // 立即执行函数结束
