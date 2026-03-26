// 主 JavaScript 文件 - 处理模态框和工具切换

// 模态框控制
function openTool(toolId) {
    const modal = document.getElementById('toolModal');
    const container = document.getElementById('toolContainer');
    
    // 根据工具 ID 加载不同的工具界面
    const toolHTML = getToolHTML(toolId);
    container.innerHTML = toolHTML;
    
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // 初始化特定工具的事件监听
    initToolEvents(toolId);
}

function closeModal() {
    const modal = document.getElementById('toolModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// 点击模态框外部关闭
window.onclick = function(event) {
    const modal = document.getElementById('toolModal');
    if (event.target === modal) {
        closeModal();
    }
}

// 获取工具 HTML
function getToolHTML(toolId) {
    const tools = {
        'litigation-cost': `
            <div class="tool-header">
                <h3>💰 诉讼费计算器</h3>
                <p>根据《诉讼费用交纳办法》计算案件受理费</p>
            </div>
            <div class="form-group">
                <label>案件类型</label>
                <select id="caseType">
                    <option value="property">财产案件</option>
                    <option value="divorce">离婚案件</option>
                    <option value="name">侵害姓名权、名称权、肖像权、名誉权、荣誉权案件</option>
                    <option value="other">其他非财产案件</option>
                    <option value="labor">劳动争议案件</option>
                    <option value="admin">行政案件</option>
                </select>
            </div>
            <div class="form-group" id="amountGroup">
                <label>诉讼标的额（元）</label>
                <input type="number" id="claimAmount" placeholder="请输入金额" min="0" step="0.01">
            </div>
            <div class="form-group" id="divorcePropertyGroup" style="display:none;">
                <label>超过 20 万元的部分金额（元）</label>
                <input type="number" id="divorcePropertyAmount" placeholder="超过 20 万的部分" min="0" step="0.01">
            </div>
            <button class="btn-calculate" onclick="calculateLitigationCost()">计算诉讼费</button>
            <div id="litigationResult" class="result-box" style="display:none;"></div>
        `,
        
        'interest': `
            <div class="tool-header">
                <h3>📈 利息计算器</h3>
                <p>计算借款利息、逾期利息、LPR 利息</p>
            </div>
            <div class="form-group">
                <label>计算类型</label>
                <select id="interestType">
                    <option value="simple">单利计算</option>
                    <option value="compound">复利计算</option>
                    <option value="lpr">LPR 利息（民间借贷）</option>
                    <option value="overdue">逾期利息</option>
                </select>
            </div>
            <div class="form-group">
                <label>本金（元）</label>
                <input type="number" id="principal" placeholder="请输入本金" min="0" step="0.01">
            </div>
            <div class="form-group">
                <label>年利率（%）</label>
                <input type="number" id="rate" placeholder="请输入年利率" min="0" step="0.01" value="3.45">
                <small style="color:#666;">当前 1 年期 LPR: 3.45%（2024 年）</small>
            </div>
            <div class="form-group">
                <label>借款日期</label>
                <input type="date" id="startDate">
            </div>
            <div class="form-group">
                <label>到期/计算日期</label>
                <input type="date" id="endDate">
            </div>
            <button class="btn-calculate" onclick="calculateInterest()">计算利息</button>
            <div id="interestResult" class="result-box" style="display:none;"></div>
        `,
        
        'workday': `
            <div class="tool-header">
                <h3>📅 工作日计算器</h3>
                <p>计算期间、期限，排除节假日和周末</p>
            </div>
            <div class="form-group">
                <label>计算类型</label>
                <select id="workdayType">
                    <option value="between">计算两个日期之间的工作日</option>
                    <option value="add">从起始日期增加 N 个工作日</option>
                    <option value="subtract">从起始日期减少 N 个工作日</option>
                </select>
            </div>
            <div class="form-group">
                <label>起始日期</label>
                <input type="date" id="workdayStart">
            </div>
            <div class="form-group" id="endDateGroup">
                <label>结束日期</label>
                <input type="date" id="workdayEnd">
            </div>
            <div class="form-group" id="daysGroup" style="display:none;">
                <label>工作日天数</label>
                <input type="number" id="workdayCount" placeholder="请输入工作日天数" min="0">
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="includeStart" checked> 包含起始日
                </label>
            </div>
            <button class="btn-calculate" onclick="calculateWorkday()">计算</button>
            <div id="workdayResult" class="result-box" style="display:none;"></div>
        `,
        
        'compensation': `
            <div class="tool-header">
                <h3>💵 赔偿金计算器</h3>
                <p>工伤、交通事故、劳动补偿金计算</p>
            </div>
            <div class="form-group">
                <label>赔偿类型</label>
                <select id="compensationType">
                    <option value="labor">经济补偿金（劳动法）</option>
                    <option value="wrongful">违法解除赔偿金（2N）</option>
                    <option value="workinjury">工伤伤残补助金</option>
                    <option value="traffic">交通事故死亡赔偿金</option>
                </select>
            </div>
            <div class="form-group">
                <label>工作年限（年）</label>
                <input type="number" id="workYears" placeholder="请输入工作年限" min="0" step="0.5">
            </div>
            <div class="form-group">
                <label>离职前 12 个月平均工资（元）</label>
                <input type="number" id="avgSalary" placeholder="请输入月平均工资" min="0" step="0.01">
            </div>
            <div class="form-group">
                <label>所在地区上年度城镇居民人均可支配收入（元/年）</label>
                <input type="number" id="localIncome" placeholder="请输入当地标准" min="0" step="0.01" value="51821">
                <small style="color:#666;">2023 年全国标准：51821 元/年</small>
            </div>
            <div class="form-group">
                <label>伤残等级（工伤适用）</label>
                <select id="disabilityLevel">
                    <option value="1">一级伤残（27 个月）</option>
                    <option value="2">二级伤残（25 个月）</option>
                    <option value="3">三级伤残（23 个月）</option>
                    <option value="4">四级伤残（21 个月）</option>
                    <option value="5">五级伤残（18 个月）</option>
                    <option value="6">六级伤残（16 个月）</option>
                    <option value="7">七级伤残（13 个月）</option>
                    <option value="8">八级伤残（11 个月）</option>
                    <option value="9">九级伤残（9 个月）</option>
                    <option value="10">十级伤残（7 个月）</option>
                </select>
            </div>
            <button class="btn-calculate" onclick="calculateCompensation()">计算赔偿金</button>
            <div id="compensationResult" class="result-box" style="display:none;"></div>
        `,
        
        'document': `
            <div class="tool-header">
                <h3>📄 法律文书生成</h3>
                <p>快速生成常用法律文书</p>
            </div>
            <div class="form-group">
                <label>文书类型</label>
                <select id="docType">
                    <option value="complaint">民事起诉状</option>
                    <option value="defense">民事答辩状</option>
                    <option value="agency">代理词</option>
                    <option value="lawyerLetter">律师函</option>
                    <option value="contract">简易合同</option>
                    <option value="power">授权委托书</option>
                </select>
            </div>
            <div class="form-group">
                <label>原告/申请人姓名</label>
                <input type="text" id="plaintiff" placeholder="请输入姓名">
            </div>
            <div class="form-group">
                <label>被告/被申请人姓名</label>
                <input type="text" id="defendant" placeholder="请输入姓名">
            </div>
            <div class="form-group">
                <label>案由/事由</label>
                <input type="text" id="cause" placeholder="例如：民间借贷纠纷">
            </div>
            <div class="form-group">
                <label>事实与理由（简要描述）</label>
                <textarea id="facts" rows="5" placeholder="请简要描述案件事实..."></textarea>
            </div>
            <div class="form-group">
                <label>诉讼请求/要求</label>
                <textarea id="requests" rows="3" placeholder="请列出具体请求..."></textarea>
            </div>
            <button class="btn-calculate" onclick="generateDocument()">生成文书</button>
            <div id="documentResult" class="result-box" style="display:none;">
                <h4>📄 生成的法律文书</h4>
                <div id="docContent" style="white-space: pre-wrap; background: white; padding: 20px; border-radius: 8px; margin-top: 15px;"></div>
                <div class="btn-group">
                    <button class="btn-secondary" onclick="copyDocument()">📋 复制</button>
                    <button class="btn-success" onclick="downloadDocument()">💾 下载</button>
                </div>
            </div>
        `,
        
        'case': `
            <div class="tool-header">
                <h3>📁 案件管理</h3>
                <p>跟踪案件进度、管理重要日期</p>
            </div>
            <div class="btn-group" style="margin-bottom: 20px;">
                <button class="btn-success" onclick="showAddCaseForm()">+ 新增案件</button>
                <button class="btn-secondary" onclick="exportCases()">📤 导出</button>
            </div>
            <div id="addCaseForm" style="display:none; background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <div class="form-group">
                    <label>案件名称</label>
                    <input type="text" id="caseName" placeholder="例如：张三诉李四借款纠纷">
                </div>
                <div class="form-group">
                    <label>案件类型</label>
                    <select id="caseCategory">
                        <option value="civil">民事案件</option>
                        <option value="criminal">刑事案件</option>
                        <option value="admin">行政案件</option>
                        <option value="arbitration">仲裁案件</option>
                        <option value="consultation">法律咨询</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>客户姓名</label>
                    <input type="text" id="clientName" placeholder="客户姓名">
                </div>
                <div class="form-group">
                    <label>联系电话</label>
                    <input type="tel" id="clientPhone" placeholder="联系电话">
                </div>
                <div class="form-group">
                    <label>重要日期</label>
                    <input type="date" id="importantDate">
                </div>
                <div class="form-group">
                    <label>备注</label>
                    <textarea id="caseNotes" rows="3" placeholder="其他备注信息..."></textarea>
                </div>
                <div class="btn-group">
                    <button class="btn-success" onclick="saveCase()">💾 保存</button>
                    <button class="btn-secondary" onclick="hideAddCaseForm()">取消</button>
                </div>
            </div>
            <div id="casesList">
                <table class="tool-table">
                    <thead>
                        <tr>
                            <th>案件名称</th>
                            <th>类型</th>
                            <th>客户</th>
                            <th>重要日期</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="casesTableBody">
                        <tr><td colspan="5" style="text-align:center;color:#666;">暂无案件，点击"新增案件"添加</td></tr>
                    </tbody>
                </table>
            </div>
        `,
        
        'timetrack': `
            <div class="tool-header">
                <h3>⏱️ 时间追踪</h3>
                <p>记录工作时长，生成计费报表</p>
            </div>
            <div class="btn-group" style="margin-bottom: 20px;">
                <button class="btn-success" id="startTimer" onclick="toggleTimer()">▶️ 开始计时</button>
                <button class="btn-secondary" onclick="addManualEntry()">+ 手动添加</button>
            </div>
            <div id="timerDisplay" style="text-align:center; padding: 30px; background: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">
                <div style="font-size: 3rem; font-weight: bold; color: #667eea;" id="timerTime">00:00:00</div>
                <div style="color: #666; margin-top: 10px;" id="timerStatus">未开始</div>
            </div>
            <div id="manualEntryForm" style="display:none; background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <div class="form-group">
                    <label>工作日期</label>
                    <input type="date" id="workDate">
                </div>
                <div class="form-group">
                    <label>工作内容</label>
                    <input type="text" id="workDescription" placeholder="例如：起草起诉状">
                </div>
                <div class="form-group">
                    <label>案件/客户</label>
                    <input type="text" id="workCase" placeholder="关联案件或客户">
                </div>
                <div class="form-group">
                    <label>工作时长（小时）</label>
                    <input type="number" id="workHours" placeholder="例如：2.5" min="0" step="0.5">
                </div>
                <div class="btn-group">
                    <button class="btn-success" onclick="saveManualEntry()">保存</button>
                    <button class="btn-secondary" onclick="hideManualEntry()">取消</button>
                </div>
            </div>
            <h4 style="margin: 20px 0 10px;">📊 时间记录</h4>
            <table class="tool-table">
                <thead>
                    <tr>
                        <th>日期</th>
                        <th>工作内容</th>
                        <th>案件/客户</th>
                        <th>时长</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody id="timeRecordsBody">
                    <tr><td colspan="5" style="text-align:center;color:#666;">暂无记录</td></tr>
                </tbody>
            </table>
            <div class="result-box" style="margin-top: 20px;">
                <h4>📈 统计汇总</h4>
                <div class="result-item">
                    <span class="result-label">本周总时长:</span>
                    <span class="result-value" id="weekTotal">0 小时</span>
                </div>
                <div class="result-item">
                    <span class="result-label">本月总时长:</span>
                    <span class="result-value" id="monthTotal">0 小时</span>
                </div>
                <div class="result-item">
                    <span class="result-label">总计:</span>
                    <span class="result-value" id="totalHours">0 小时</span>
                </div>
            </div>
        `,
        
        'lawsearch': `
            <div class="tool-header">
                <h3>🔍 法条检索</h3>
                <p>快速查找相关法律法规（本地数据库）</p>
            </div>
            <div class="form-group">
                <label>搜索关键词</label>
                <input type="text" id="lawKeyword" placeholder="例如：合同、侵权、婚姻...">
            </div>
            <div class="form-group">
                <label>法律类别</label>
                <select id="lawCategory">
                    <option value="all">全部</option>
                    <option value="civil">民法典</option>
                    <option value="criminal">刑法</option>
                    <option value="procedure">诉讼法</option>
                    <option value="labor">劳动法</option>
                    <option value="company">公司法</option>
                    <option value="contract">合同法</option>
                </select>
            </div>
            <button class="btn-calculate" onclick="searchLaw()">搜索</button>
            <div id="lawResults" style="margin-top: 20px;"></div>
        `
    };
    
    return tools[toolId] || '<p>工具加载中...</p>';
}

// 初始化工具事件
function initToolEvents(toolId) {
    // 诉讼费计算器 - 显示/隐藏金额输入
    if (toolId === 'litigation-cost') {
        const caseType = document.getElementById('caseType');
        if (caseType) {
            caseType.addEventListener('change', function() {
                const amountGroup = document.getElementById('amountGroup');
                const divorcePropertyGroup = document.getElementById('divorcePropertyGroup');
                
                if (this.value === 'divorce') {
                    divorcePropertyGroup.style.display = 'block';
                } else {
                    divorcePropertyGroup.style.display = 'none';
                }
                
                if (['property', 'divorce'].includes(this.value)) {
                    amountGroup.style.display = 'block';
                } else {
                    amountGroup.style.display = 'none';
                }
            });
        }
        
        // 设置默认日期
        const today = new Date().toISOString().split('T')[0];
        const startDate = document.getElementById('startDate');
        const endDate = document.getElementById('endDate');
        if (startDate) startDate.value = today;
        if (endDate) {
            const nextMonth = new Date();
            nextMonth.setMonth(nextMonth.getMonth() + 1);
            endDate.value = nextMonth.toISOString().split('T')[0];
        }
    }
    
    // 工作日计算器 - 显示/隐藏输入
    if (toolId === 'workday') {
        const workdayType = document.getElementById('workdayType');
        if (workdayType) {
            workdayType.addEventListener('change', function() {
                const endDateGroup = document.getElementById('endDateGroup');
                const daysGroup = document.getElementById('daysGroup');
                
                if (this.value === 'between') {
                    endDateGroup.style.display = 'block';
                    daysGroup.style.display = 'none';
                } else {
                    endDateGroup.style.display = 'none';
                    daysGroup.style.display = 'block';
                }
            });
        }
        
        const today = new Date().toISOString().split('T')[0];
        const workdayStart = document.getElementById('workdayStart');
        const workdayEnd = document.getElementById('workdayEnd');
        if (workdayStart) workdayStart.value = today;
        if (workdayEnd) {
            const nextWeek = new Date();
            nextWeek.setDate(nextWeek.getDate() + 7);
            workdayEnd.value = nextWeek.toISOString().split('T')[0];
        }
    }
    
    // 案件管理 - 加载案件列表
    if (toolId === 'case') {
        loadCases();
    }
    
    // 时间追踪 - 加载记录和更新统计
    if (toolId === 'timetrack') {
        loadTimeRecords();
        updateTimeStats();
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.style.borderLeftColor = type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#667eea';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// 格式化金额
function formatMoney(amount) {
    return '¥' + parseFloat(amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

// 格式化数字
function formatNumber(num) {
    return parseFloat(num).toLocaleString('zh-CN');
}
