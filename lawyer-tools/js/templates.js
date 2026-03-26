// 模板和管理功能模块

/**
 * 加载文书模板
 */
function loadTemplate(templateId) {
    const templates = {
        'civil-complaint': `民事起诉状

原告：[姓名]，[性别]，[民族]，[出生日期]，[身份证号]
住址：[详细地址]
联系电话：[电话号码]

被告：[姓名]，[性别]，[民族]，[出生日期]，[身份证号]
住址：[详细地址]
联系电话：[电话号码]

案由：[例如：民间借贷纠纷/买卖合同纠纷/离婚纠纷等]

诉讼请求：
1. 请求判令被告 [具体请求内容，如：偿还原告借款本金 XX 元及利息 XX 元]；
2. 请求判令被告承担本案全部诉讼费用。

事实与理由：
[详细陈述案件事实，包括：
- 事件发生的时间、地点
- 双方的权利义务关系
- 被告违约或侵权的具体行为
- 给原告造成的损失
- 法律依据]

综上所述，被告的行为严重侵害了原告的合法权益。为维护原告的合法权益，特向贵院提起诉讼，恳请贵院依法支持原告的全部诉讼请求。

此致
[XXX] 人民法院

具状人（签字）：__________
[年] 年 [月] 月 [日] 日

附：
1. 本起诉状副本 [X] 份
2. 原告身份证复印件 1 份
3. 证据清单及证据材料 [X] 份
`,
        
        'defense': `民事答辩状

答辩人（被告）：[姓名]，[性别]，[民族]，[出生日期]，[身份证号]
住址：[详细地址]
联系电话：[电话号码]

被答辩人（原告）：[姓名]，[性别]，[民族]，[出生日期]，[身份证号]
住址：[详细地址]

答辩人就 [案由] 一案（案号：[XXXX]），针对被答辩人的起诉，提出如下答辩意见：

一、关于本案的基本事实
[陈述答辩人认为的案件事实，可与原告陈述有所不同]

二、对原告诉请的答辩意见
1. 关于 [原告第一项请求]：
   [详细答辩意见，可承认、否认或部分承认]

2. 关于 [原告第二项请求]：
   [详细答辩意见]

三、法律依据
[引用支持答辩意见的相关法律规定]

四、答辩请求
综上所述，答辩人请求贵院：
1. [例如：驳回原告的全部诉讼请求]；
2. [或：依法改判...]；
3. 本案诉讼费用由 [原告/双方] 承担。

此致
[XXX] 人民法院

答辩人（签字）：__________
[年] 年 [月] 月 [日] 日

附：
1. 本答辩状副本 [X] 份
2. 证据清单及证据材料 [X] 份
`,
        
        'agency-opinion': `代理词

审判长、审判员（或人民陪审员）：

[XXX] 律师事务所接受本案 [原告/被告/上诉人/被上诉人] [当事人姓名] 的委托，指派我担任其诉讼代理人。接受委托后，代理人详细了解了案情，进行了必要的调查取证，现结合庭审情况，发表如下代理意见：

一、案件基本情况
[简要概述案件背景、当事人关系、争议焦点等]

二、本案争议焦点
[归纳本案的核心争议点，通常 2-3 个]

三、代理意见

（一）关于 [争议焦点一]
1. 事实层面：[详细论述]
2. 法律层面：[引用法条，进行分析]
3. 结论：[得出对委托人有利的结论]

（二）关于 [争议焦点二]
1. 事实层面：[详细论述]
2. 法律层面：[引用法条，进行分析]
3. 结论：[得出对委托人有利的结论]

四、总结
综上所述，[重申核心观点]。恳请合议庭充分考虑代理人的上述意见，依法作出公正裁判。

此致
[XXX] 人民法院

代理人：[XXX] 律师
[XXX] 律师事务所
[年] 年 [月] 月 [日] 日
`,
        
        'lawyer-letter': `律师函

[XXXX] 律函字第 [XX] 号

[收件人姓名/公司名称]：

[XXX] 律师事务所（以下简称"本所"）系根据中华人民共和国法律合法注册并存续的律师事务所，执业许可证号：[XXXXXX]。本所依法接受 [委托人姓名/公司名称]（以下简称"委托人"）的委托，指派 [XXX] 律师（以下简称"本律师"）就 [事由] 一事，郑重致函如下：

一、事实概要
根据委托人提供的材料及陈述：
1. [事实一]
2. [事实二]
3. [事实三]

二、法律分析
本律师经审慎研究后认为：
1. 根据《[相关法律名称]》第 [X] 条规定：[法条内容]
2. [分析对方行为的违法性或违约性]
3. [说明对方应承担的法律责任]

三、律师意见及要求
基于上述事实与法律分析，本律师代表委托人郑重提出如下要求：
1. 请贵方于收到本函之日起 [X] 日内，[具体要求，如：支付欠款 XX 元]；
2. [其他要求]；
3. 请贵方指定专人与本律师联系，协商解决方案。

四、法律后果告知
如贵方未在上述期限内履行上述义务，本所将依委托人授权，采取包括但不限于以下法律措施：
1. 向有管辖权的人民法院提起诉讼；
2. 申请财产保全；
3. 向相关行政主管部门投诉举报；
4. 通过媒体公开披露相关信息。

届时，贵方除需履行上述义务外，还可能承担诉讼费、律师费、保全费、执行费等额外费用，并可能面临信用记录受损等不利后果。

望贵方慎重对待，以免讼累。

特此函告！

[XXX] 律师事务所
[XXX] 律师
联系电话：[电话号码]
电子邮箱：[邮箱地址]
[年] 年 [月] 月 [日] 日

（律师事务所盖章）
`,
        
        'contract': `合 同 书

合同编号：[XXXXXX]

甲方（[例如：出卖方/出租方/服务提供方]）：[姓名/公司名称]
统一社会信用代码/身份证号：[XXXXXX]
住所地：[详细地址]
法定代表人/负责人：[姓名]
联系电话：[电话号码]

乙方（[例如：买受方/承租方/服务接受方]）：[姓名/公司名称]
统一社会信用代码/身份证号：[XXXXXX]
住所地：[详细地址]
法定代表人/负责人：[姓名]
联系电话：[电话号码]

鉴于 [合同背景说明]，甲乙双方经平等协商，根据《中华人民共和国民法典》及相关法律法规，达成如下协议：

第一条 [合同标的/服务内容]
1.1 [具体内容]
1.2 [具体内容]

第二条 合同价款及支付方式
2.1 合同总价款：人民币 [XX] 元（大写：[XX 元整]）
2.2 支付方式：[银行转账/现金/其他]
2.3 支付时间：[具体时间或节点]
2.4 甲方收款账户信息：
   户名：[XXX]
   开户行：[XXX]
   账号：[XXX]

第三条 履行期限、地点和方式
3.1 履行期限：自 [年] 年 [月] 月 [日] 日起至 [年] 年 [月] 月 [日] 日止
3.2 履行地点：[详细地址]
3.3 履行方式：[具体方式]

第四条 双方权利义务
4.1 甲方权利义务：
   (1) [权利一]
   (2) [权利二]
   (3) [义务一]
   (4) [义务二]

4.2 乙方权利义务：
   (1) [权利一]
   (2) [权利二]
   (3) [义务一]
   (4) [义务二]

第五条 违约责任
5.1 甲方违约责任：[具体约定]
5.2 乙方违约责任：[具体约定]
5.3 违约金：[金额或计算方式]

第六条 争议解决
6.1 本合同履行过程中发生争议，双方应友好协商解决。
6.2 协商不成的，任何一方均可向 [甲方所在地/乙方所在地/合同履行地] 有管辖权的人民法院提起诉讼。

第七条 其他约定
7.1 本合同自双方签字（盖章）之日起生效。
7.2 本合同一式 [X] 份，甲乙双方各执 [X] 份，具有同等法律效力。
7.3 [其他补充条款]

（以下无正文）

甲方（盖章）：__________        乙方（盖章）：__________
法定代表人/授权代表：__________  法定代表人/授权代表：__________
签订日期：[年] 年 [月] 月 [日] 日  签订日期：[年] 年 [月] 月 [日] 日
签订地点：[城市名称]            签订地点：[城市名称]
`,
        
        'power-attorney': `授权委托书

委托人：[姓名]，[性别]，[民族]，[出生日期]
身份证号：[XXXXXXXXXXXXXXXXXX]
住址：[详细地址]
联系电话：[电话号码]

受托人：[律师姓名]，[XXX] 律师事务所执业律师
执业证号：[XXXXXXXXXX]
联系电话：[电话号码]

现委托人因与 [对方当事人姓名][案由] 纠纷一案，特委托上列受托人作为委托人的诉讼代理人。

代理权限：

【选择一：一般代理】
□ 一般代理：代为起诉、应诉，参加庭审，陈述事实，提供证据，进行辩论，代为签收法律文书等。

【选择二：特别授权】
☑ 特别授权代理：除一般代理权限外，还包括以下权限：
□ 代为承认、放弃、变更诉讼请求；
□ 进行和解；
□ 提起反诉；
□ 提起上诉；
□ 代为申请执行；
□ 代为收取/支付款项；
□ 其他：[具体说明]

代理期限：
自本授权委托书签署之日起，至本案 [一审/二审/执行] 程序终结之日止。

委托人确认：受托人在上述代理权限内所实施的法律行为及签署的法律文件，委托人均予以承认并承担相应的法律后果。

委托人（签字并按指印）：__________
受托人（签字）：__________

签署日期：[年] 年 [月] 月 [日] 日

附：
1. 委托人身份证复印件 1 份
2. 受托人律师执业证复印件 1 份
3. 律师事务所函 1 份
`
    };
    
    const template = templates[templateId];
    if (template) {
        // 打开文书生成工具并填入模板
        openTool('document');
        setTimeout(() => {
            const docContent = document.getElementById('docContent');
            if (docContent) {
                docContent.textContent = template;
                window.currentDocument = template;
                showNotification('模板已加载，可根据具体案情修改', 'success');
            }
        }, 300);
    }
}

/**
 * 案件管理功能
 */
// 显示新增案件表单
function showAddCaseForm() {
    document.getElementById('addCaseForm').style.display = 'block';
    document.getElementById('caseName').value = '';
    document.getElementById('clientName').value = '';
    document.getElementById('clientPhone').value = '';
    document.getElementById('importantDate').value = '';
    document.getElementById('caseNotes').value = '';
}

function hideAddCaseForm() {
    document.getElementById('addCaseForm').style.display = 'none';
}

// 保存案件
function saveCase() {
    const caseData = {
        id: Date.now(),
        name: document.getElementById('caseName').value,
        category: document.getElementById('caseCategory').value,
        client: document.getElementById('clientName').value,
        phone: document.getElementById('clientPhone').value,
        date: document.getElementById('importantDate').value,
        notes: document.getElementById('caseNotes').value,
        createdAt: new Date().toISOString()
    };
    
    if (!caseData.name) {
        showNotification('请输入案件名称', 'error');
        return;
    }
    
    // 获取现有案件
    let cases = JSON.parse(localStorage.getItem('lawyerCases') || '[]');
    cases.push(caseData);
    localStorage.setItem('lawyerCases', JSON.stringify(cases));
    
    hideAddCaseForm();
    loadCases();
    showNotification('案件已保存', 'success');
}

// 加载案件列表
function loadCases() {
    const cases = JSON.parse(localStorage.getItem('lawyerCases') || '[]');
    const tbody = document.getElementById('casesTableBody');
    
    if (cases.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#666;">暂无案件，点击"新增案件"添加</td></tr>';
        return;
    }
    
    const categoryNames = {
        'civil': '民事',
        'criminal': '刑事',
        'admin': '行政',
        'arbitration': '仲裁',
        'consultation': '咨询'
    };
    
    tbody.innerHTML = cases.map(caseItem => `
        <tr>
            <td>${caseItem.name}</td>
            <td>${categoryNames[caseItem.category] || caseItem.category}</td>
            <td>${caseItem.client || '-'}${caseItem.phone ? `<br><small style="color:#666;">${caseItem.phone}</small>` : ''}</td>
            <td>${caseItem.date || '-'}</td>
            <td>
                <button class="btn-secondary" style="padding:5px 10px;font-size:0.85rem;" onclick="deleteCase(${caseItem.id})">删除</button>
            </td>
        </tr>
    `).join('');
}

// 删除案件
function deleteCase(caseId) {
    if (!confirm('确定要删除这个案件吗？')) return;
    
    let cases = JSON.parse(localStorage.getItem('lawyerCases') || '[]');
    cases = cases.filter(c => c.id !== caseId);
    localStorage.setItem('lawyerCases', JSON.stringify(cases));
    
    loadCases();
    showNotification('案件已删除', 'success');
}

// 导出案件
function exportCases() {
    const cases = JSON.parse(localStorage.getItem('lawyerCases') || '[]');
    if (cases.length === 0) {
        showNotification('暂无案件可导出', 'error');
        return;
    }
    
    const csvContent = [
        ['案件名称', '类型', '客户', '电话', '重要日期', '备注', '创建时间'],
        ...cases.map(c => [
            c.name,
            c.category,
            c.client,
            c.phone,
            c.date,
            c.notes,
            c.createdAt
        ])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `案件列表_${new Date().toLocaleDateString('zh-CN').replace(/\//g, '-')}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    
    showNotification('案件已导出', 'success');
}

/**
 * 时间追踪功能
 */
let timerInterval = null;
let timerSeconds = 0;
let timerRunning = false;
let currentWorkDescription = '';
let currentWorkCase = '';

// 切换计时器
function toggleTimer() {
    const btn = document.getElementById('startTimer');
    const status = document.getElementById('timerStatus');
    
    if (timerRunning) {
        // 停止计时
        clearInterval(timerInterval);
        timerRunning = false;
        btn.textContent = '▶️ 开始计时';
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-success');
        status.textContent = '已暂停';
        
        // 保存记录
        saveTimeRecord({
            date: new Date().toISOString().split('T')[0],
            description: currentWorkDescription || '未命名工作',
            case: currentWorkCase || '-',
            seconds: timerSeconds
        });
        
        timerSeconds = 0;
        currentWorkDescription = '';
        currentWorkCase = '';
    } else {
        // 开始计时
        // 先询问工作内容和案件
        currentWorkDescription = prompt('请输入工作内容：', '法律咨询') || '未命名工作';
        currentWorkCase = prompt('请输入案件/客户名称：', '-') || '-';
        
        timerRunning = true;
        btn.textContent = '⏹️ 停止计时';
        btn.classList.remove('btn-success');
        btn.classList.add('btn-danger');
        status.textContent = '计时中...';
        
        timerInterval = setInterval(() => {
            timerSeconds++;
            updateTimerDisplay();
        }, 1000);
    }
}

// 更新计时器显示
function updateTimerDisplay() {
    const hours = Math.floor(timerSeconds / 3600);
    const minutes = Math.floor((timerSeconds % 3600) / 60);
    const seconds = timerSeconds % 60;
    
    document.getElementById('timerTime').textContent = 
        `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// 显示手动添加表单
function addManualEntry() {
    document.getElementById('manualEntryForm').style.display = 'block';
    document.getElementById('workDate').value = new Date().toISOString().split('T')[0];
    document.getElementById('workDescription').value = '';
    document.getElementById('workCase').value = '';
    document.getElementById('workHours').value = '';
}

function hideManualEntry() {
    document.getElementById('manualEntryForm').style.display = 'none';
}

// 保存手动添加的记录
function saveManualEntry() {
    const record = {
        date: document.getElementById('workDate').value,
        description: document.getElementById('workDescription').value,
        case: document.getElementById('workCase').value,
        seconds: (parseFloat(document.getElementById('workHours').value) || 0) * 3600
    };
    
    if (!record.date || !record.description) {
        showNotification('请填写完整信息', 'error');
        return;
    }
    
    saveTimeRecord(record);
    hideManualEntry();
    loadTimeRecords();
    updateTimeStats();
    showNotification('记录已保存', 'success');
}

// 保存时间记录
function saveTimeRecord(record) {
    if (record.seconds < 60) return; // 少于 1 分钟不保存
    
    let records = JSON.parse(localStorage.getItem('timeRecords') || '[]');
    records.push({
        ...record,
        id: Date.now(),
        createdAt: new Date().toISOString()
    });
    localStorage.setItem('timeRecords', JSON.stringify(records));
}

// 加载时间记录
function loadTimeRecords() {
    const records = JSON.parse(localStorage.getItem('timeRecords') || '[]');
    const tbody = document.getElementById('timeRecordsBody');
    
    if (records.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#666;">暂无记录</td></tr>';
        return;
    }
    
    // 按时间倒序排列
    records.sort((a, b) => b.id - a.id);
    
    tbody.innerHTML = records.map(record => {
        const hours = (record.seconds / 3600).toFixed(2);
        return `
            <tr>
                <td>${record.date}</td>
                <td>${record.description}</td>
                <td>${record.case}</td>
                <td>${hours} 小时</td>
                <td>
                    <button class="btn-danger" style="padding:5px 10px;font-size:0.85rem;" onclick="deleteTimeRecord(${record.id})">删除</button>
                </td>
            </tr>
        `;
    }).join('');
}

// 删除时间记录
function deleteTimeRecord(recordId) {
    if (!confirm('确定要删除这条记录吗？')) return;
    
    let records = JSON.parse(localStorage.getItem('timeRecords') || '[]');
    records = records.filter(r => r.id !== recordId);
    localStorage.setItem('timeRecords', JSON.stringify(records));
    
    loadTimeRecords();
    updateTimeStats();
    showNotification('记录已删除', 'success');
}

// 更新时间统计
function updateTimeStats() {
    const records = JSON.parse(localStorage.getItem('timeRecords') || '[]');
    
    const now = new Date();
    const currentWeekStart = new Date(now);
    currentWeekStart.setDate(now.getDate() - now.getDay());
    currentWeekStart.setHours(0, 0, 0, 0);
    
    const currentMonthStart = new Date(now.getFullYear(), now.getMonth(), 1);
    
    let weekSeconds = 0;
    let monthSeconds = 0;
    let totalSeconds = 0;
    
    records.forEach(record => {
        const recordDate = new Date(record.date);
        totalSeconds += record.seconds;
        
        if (recordDate >= currentWeekStart) {
            weekSeconds += record.seconds;
        }
        
        if (recordDate >= currentMonthStart) {
            monthSeconds += record.seconds;
        }
    });
    
    document.getElementById('weekTotal').textContent = `${(weekSeconds / 3600).toFixed(2)} 小时`;
    document.getElementById('monthTotal').textContent = `${(monthSeconds / 3600).toFixed(2)} 小时`;
    document.getElementById('totalHours').textContent = `${(totalSeconds / 3600).toFixed(2)} 小时`;
}
