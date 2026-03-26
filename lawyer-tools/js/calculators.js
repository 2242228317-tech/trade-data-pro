// 计算器功能模块

/**
 * 诉讼费计算
 * 根据《诉讼费用交纳办法》第十三条
 */
function calculateLitigationCost() {
    const caseType = document.getElementById('caseType').value;
    const amount = parseFloat(document.getElementById('claimAmount').value) || 0;
    const divorcePropertyAmount = parseFloat(document.getElementById('divorcePropertyAmount').value) || 0;
    
    let cost = 0;
    let detail = [];
    
    switch (caseType) {
        case 'property':
            // 财产案件分段累计
            if (amount <= 10000) {
                cost = 50;
                detail.push('1 万元以下：50 元');
            } else if (amount <= 100000) {
                cost = 50 + (amount - 10000) * 0.025;
                detail.push('1 万元以下：50 元');
                detail.push(`1 万 -10 万元部分：${formatMoney((amount - 10000) * 0.025)}`);
            } else if (amount <= 200000) {
                cost = 50 + 90000 * 0.025 + (amount - 100000) * 0.02;
                detail.push('1 万元以下：50 元');
                detail.push('1 万 -10 万元部分：2,250 元');
                detail.push(`10 万 -20 万元部分：${formatMoney((amount - 100000) * 0.02)}`);
            } else if (amount <= 500000) {
                cost = 50 + 90000 * 0.025 + 100000 * 0.02 + (amount - 200000) * 0.015;
                detail.push('1 万元以下：50 元');
                detail.push('1 万 -10 万元部分：2,250 元');
                detail.push('10 万 -20 万元部分：2,000 元');
                detail.push(`20 万 -50 万元部分：${formatMoney((amount - 200000) * 0.015)}`);
            } else if (amount <= 1000000) {
                cost = 50 + 90000 * 0.025 + 100000 * 0.02 + 300000 * 0.015 + (amount - 500000) * 0.01;
                detail.push('1 万元以下：50 元');
                detail.push('1 万 -10 万元部分：2,250 元');
                detail.push('10 万 -20 万元部分：2,000 元');
                detail.push('20 万 -50 万元部分：4,500 元');
                detail.push(`50 万 -100 万元部分：${formatMoney((amount - 500000) * 0.01)}`);
            } else if (amount <= 2000000) {
                cost = 50 + 90000 * 0.025 + 100000 * 0.02 + 300000 * 0.015 + 500000 * 0.01 + (amount - 1000000) * 0.009;
                detail.push('1 万元以下：50 元');
                detail.push('1 万 -10 万元部分：2,250 元');
                detail.push('10 万 -20 万元部分：2,000 元');
                detail.push('20 万 -50 万元部分：4,500 元');
                detail.push('50 万 -100 万元部分：5,000 元');
                detail.push(`100 万 -200 万元部分：${formatMoney((amount - 1000000) * 0.009)}`);
            } else if (amount <= 5000000) {
                cost = 50 + 90000 * 0.025 + 100000 * 0.02 + 300000 * 0.015 + 500000 * 0.01 + 1000000 * 0.009 + (amount - 2000000) * 0.008;
                detail.push('1 万元以下：50 元');
                detail.push('1 万 -10 万元部分：2,250 元');
                detail.push('10 万 -20 万元部分：2,000 元');
                detail.push('20 万 -50 万元部分：4,500 元');
                detail.push('50 万 -100 万元部分：5,000 元');
                detail.push('100 万 -200 万元部分：9,000 元');
                detail.push(`200 万 -500 万元部分：${formatMoney((amount - 2000000) * 0.008)}`);
            } else if (amount <= 10000000) {
                cost = 50 + 90000 * 0.025 + 100000 * 0.02 + 300000 * 0.015 + 500000 * 0.01 + 1000000 * 0.009 + 3000000 * 0.008 + (amount - 5000000) * 0.007;
                detail.push('1 万元以下：50 元');
                detail.push('1 万 -10 万元部分：2,250 元');
                detail.push('10 万 -20 万元部分：2,000 元');
                detail.push('20 万 -50 万元部分：4,500 元');
                detail.push('50 万 -100 万元部分：5,000 元');
                detail.push('100 万 -200 万元部分：9,000 元');
                detail.push('200 万 -500 万元部分：24,000 元');
                detail.push(`500 万 -1000 万元部分：${formatMoney((amount - 5000000) * 0.007)}`);
            } else {
                cost = 50 + 90000 * 0.025 + 100000 * 0.02 + 300000 * 0.015 + 500000 * 0.01 + 1000000 * 0.009 + 3000000 * 0.008 + 5000000 * 0.007 + (amount - 10000000) * 0.005;
                detail.push('1 万元以下：50 元');
                detail.push('1 万 -10 万元部分：2,250 元');
                detail.push('10 万 -20 万元部分：2,000 元');
                detail.push('20 万 -50 万元部分：4,500 元');
                detail.push('50 万 -100 万元部分：5,000 元');
                detail.push('100 万 -200 万元部分：9,000 元');
                detail.push('200 万 -500 万元部分：24,000 元');
                detail.push('500 万 -1000 万元部分：35,000 元');
                detail.push(`1000 万元以上部分：${formatMoney((amount - 10000000) * 0.005)}`);
            }
            break;
            
        case 'divorce':
            cost = 200;
            detail.push('基础受理费：200 元');
            if (divorcePropertyAmount > 0) {
                const propertyFee = divorcePropertyAmount * 0.005;
                cost += propertyFee;
                detail.push(`超过 20 万元部分 (0.5%)：${formatMoney(propertyFee)}`);
            }
            break;
            
        case 'name':
            cost = 200;
            detail.push('受理费：200 元');
            if (amount > 0) {
                detail.push(`涉及金额：${formatMoney(amount)} 元`);
            }
            break;
            
        case 'other':
            cost = 80;
            detail.push('受理费：80 元');
            break;
            
        case 'labor':
            cost = 10;
            detail.push('劳动争议案件：10 元');
            break;
            
        case 'admin':
            cost = 50;
            detail.push('行政案件：50 元');
            break;
    }
    
    // 显示结果
    const resultDiv = document.getElementById('litigationResult');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <h4>📊 诉讼费计算结果</h4>
        ${detail.map(d => `<div class="result-item"><span class="result-label">${d.split('：')[0]}</span><span class="result-value">${d.split('：')[1]}</span></div>`).join('')}
        <div class="result-item">
            <span class="result-label">合计受理费:</span>
            <span class="result-value">${formatMoney(cost)}</span>
        </div>
        <p style="margin-top:15px;font-size:0.9rem;color:#666;">
            💡 提示：以上计算仅供参考，具体金额以法院核定为准。减半收取情形、简易程序等可能影响最终费用。
        </p>
    `;
}

/**
 * 利息计算
 */
function calculateInterest() {
    const interestType = document.getElementById('interestType').value;
    const principal = parseFloat(document.getElementById('principal').value) || 0;
    const rate = parseFloat(document.getElementById('rate').value) || 0;
    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);
    
    if (principal <= 0) {
        showNotification('请输入有效的本金金额', 'error');
        return;
    }
    
    // 计算天数
    const days = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
    const years = days / 365;
    
    let interest = 0;
    let detail = [];
    
    switch (interestType) {
        case 'simple':
            // 单利
            interest = principal * (rate / 100) * years;
            detail.push(`计算公式：本金 × 年利率 × 年数`);
            detail.push(`${formatMoney(principal)} × ${rate}% × ${years.toFixed(4)}年`);
            break;
            
        case 'compound':
            // 复利（按月复利）
            const monthlyRate = rate / 100 / 12;
            const months = days / 30;
            interest = principal * Math.pow(1 + monthlyRate, months) - principal;
            detail.push(`计算公式：本金 × (1 + 月利率)^月数 - 本金`);
            detail.push(`月利率：${(monthlyRate * 100).toFixed(4)}%`);
            detail.push(`计息月数：${months.toFixed(2)}个月`);
            break;
            
        case 'lpr':
            // LPR 利息（民间借贷，支持 4 倍 LPR）
            const lprRate = 3.45; // 当前 1 年期 LPR
            const maxRate = lprRate * 4;
            const usedRate = Math.min(rate, maxRate);
            interest = principal * (usedRate / 100) * years;
            detail.push(`当前 1 年期 LPR: ${lprRate}%`);
            detail.push(`4 倍 LPR 上限：${maxRate}%`);
            detail.push(`实际适用利率：${usedRate}%`);
            if (rate > maxRate) {
                detail.push(`⚠️ 约定利率${rate}% 超过 4 倍 LPR，超出部分不受法律保护`);
            }
            break;
            
        case 'overdue':
            // 逾期利息（按日利率万分之五计算）
            const dailyRate = 0.0005;
            interest = principal * dailyRate * days;
            detail.push(`逾期利率：日利率 0.05%（万分之五）`);
            detail.push(`逾期天数：${days}天`);
            break;
    }
    
    // 显示结果
    const resultDiv = document.getElementById('interestResult');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <h4>📊 利息计算结果</h4>
        <div class="result-item">
            <span class="result-label">本金:</span>
            <span class="result-value">${formatMoney(principal)}</span>
        </div>
        <div class="result-item">
            <span class="result-label">计息期间:</span>
            <span class="result-value">${startDate.toLocaleDateString()} 至 ${endDate.toLocaleDateString()} (${days}天)</span>
        </div>
        ${detail.map(d => `<div class="result-item"><span class="result-label">${d.split('：')[0]}</span><span class="result-value">${d.split('：')[1] || d}</span></div>`).join('')}
        <div class="result-item">
            <span class="result-label">利息总额:</span>
            <span class="result-value">${formatMoney(interest)}</span>
        </div>
        <div class="result-item">
            <span class="result-label">本息合计:</span>
            <span class="result-value">${formatMoney(principal + interest)}</span>
        </div>
    `;
}

/**
 * 工作日计算
 */
function calculateWorkday() {
    const workdayType = document.getElementById('workdayType').value;
    const startDate = new Date(document.getElementById('workdayStart').value);
    const includeStart = document.getElementById('includeStart').checked;
    
    let resultText = '';
    let resultDate = null;
    let workdays = 0;
    
    if (workdayType === 'between') {
        const endDate = new Date(document.getElementById('workdayEnd').value);
        workdays = countWorkdays(startDate, endDate, includeStart);
        resultText = `从 ${startDate.toLocaleDateString()} 到 ${endDate.toLocaleDateString()} 共有 <strong>${workdays}</strong> 个工作日`;
    } else if (workdayType === 'add') {
        const days = parseInt(document.getElementById('workdayCount').value) || 0;
        resultDate = addWorkdays(startDate, days, includeStart);
        workdays = days;
        resultText = `从 ${startDate.toLocaleDateString()} 起第 ${days} 个工作日是 <strong>${resultDate.toLocaleDateString()}</strong>`;
    } else if (workdayType === 'subtract') {
        const days = parseInt(document.getElementById('workdayCount').value) || 0;
        resultDate = addWorkdays(startDate, -days, includeStart);
        workdays = -days;
        resultText = `从 ${startDate.toLocaleDateString()} 往前推 ${Math.abs(days)} 个工作日是 <strong>${resultDate.toLocaleDateString()}</strong>`;
    }
    
    // 显示结果
    const resultDiv = document.getElementById('workdayResult');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <h4>📅 计算结果</h4>
        <p style="font-size:1.1rem;margin:15px 0;">${resultText}</p>
        <p style="color:#666;font-size:0.9rem;">
            💡 提示：本计算仅排除周六、周日，未考虑法定节假日。实际工作中请结合当年放假安排。
        </p>
    `;
}

// 计算两个日期之间的工作日天数
function countWorkdays(start, end, includeStart) {
    let count = 0;
    const current = new Date(start);
    const end_date = new Date(end);
    
    if (!includeStart) {
        current.setDate(current.getDate() + 1);
    }
    
    while (current <= end_date) {
        const day = current.getDay();
        if (day !== 0 && day !== 6) { // 排除周日 (0) 和周六 (6)
            count++;
        }
        current.setDate(current.getDate() + 1);
    }
    
    return count;
}

// 增加/减少工作日
function addWorkdays(start, days, includeStart) {
    const result = new Date(start);
    if (!includeStart) {
        result.setDate(result.getDate() + 1);
    }
    
    let remaining = Math.abs(days);
    const direction = days >= 0 ? 1 : -1;
    
    while (remaining > 0) {
        result.setDate(result.getDate() + direction);
        const day = result.getDay();
        if (day !== 0 && day !== 6) {
            remaining--;
        }
    }
    
    return result;
}

/**
 * 赔偿金计算
 */
function calculateCompensation() {
    const compType = document.getElementById('compensationType').value;
    const workYears = parseFloat(document.getElementById('workYears').value) || 0;
    const avgSalary = parseFloat(document.getElementById('avgSalary').value) || 0;
    const localIncome = parseFloat(document.getElementById('localIncome').value) || 0;
    const disabilityLevel = parseInt(document.getElementById('disabilityLevel').value) || 10;
    
    let compensation = 0;
    let detail = [];
    
    // 伤残等级对应的月数
    const disabilityMonths = {
        1: 27, 2: 25, 3: 23, 4: 21, 5: 18, 6: 16,
        7: 13, 8: 11, 9: 9, 10: 7
    };
    
    switch (compType) {
        case 'labor':
            // 经济补偿金 N
            compensation = workYears * avgSalary;
            detail.push(`工作年限：${workYears}年`);
            detail.push(`月平均工资：${formatMoney(avgSalary)}`);
            detail.push(`计算标准：N（每年 1 个月工资）`);
            break;
            
        case 'wrongful':
            // 违法解除赔偿金 2N
            compensation = 2 * workYears * avgSalary;
            detail.push(`工作年限：${workYears}年`);
            detail.push(`月平均工资：${formatMoney(avgSalary)}`);
            detail.push(`计算标准：2N（违法解除双倍赔偿）`);
            break;
            
        case 'workinjury':
            // 工伤一次性伤残补助金
            const months = disabilityMonths[disabilityLevel] || 7;
            compensation = months * avgSalary;
            detail.push(`伤残等级：${disabilityLevel}级`);
            detail.push(`本人工资：${formatMoney(avgSalary)}`);
            detail.push(`补助月数：${months}个月`);
            break;
            
        case 'traffic':
            // 交通事故死亡赔偿金（20 年）
            compensation = localIncome * 20;
            detail.push(`上年度城镇居民人均可支配收入：${formatMoney(localIncome)}元/年`);
            detail.push(`赔偿年限：20 年`);
            break;
    }
    
    // 显示结果
    const resultDiv = document.getElementById('compensationResult');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <h4>💵 赔偿金计算结果</h4>
        ${detail.map(d => `<div class="result-item"><span class="result-label">${d.split('：')[0]}</span><span class="result-value">${d.split('：')[1] || d}</span></div>`).join('')}
        <div class="result-item">
            <span class="result-label">赔偿金额:</span>
            <span class="result-value">${formatMoney(compensation)}</span>
        </div>
        <p style="margin-top:15px;font-size:0.9rem;color:#666;">
            💡 提示：以上计算仅供参考，实际赔偿需结合具体案情和当地标准。建议咨询专业律师。
        </p>
    `;
}

/**
 * 生成法律文书
 */
function generateDocument() {
    const docType = document.getElementById('docType').value;
    const plaintiff = document.getElementById('plaintiff').value || 'XXX';
    const defendant = document.getElementById('defendant').value || 'XXX';
    const cause = document.getElementById('cause').value || 'XXX 纠纷';
    const facts = document.getElementById('facts').value || '事实与理由待补充...';
    const requests = document.getElementById('requests').value || '诉讼请求待补充...';
    
    let docContent = '';
    const today = new Date().toLocaleDateString('zh-CN');
    
    switch (docType) {
        case 'complaint':
            docContent = `民事起诉状

原告：${plaintiff}
被告：${defendant}

案由：${cause}

诉讼请求：
${requests}

事实与理由：
${facts}

此致
XXX 人民法院

具状人：${plaintiff}
${today}

附：
1. 本起诉状副本 X 份
2. 证据清单及证据材料
`;
            break;
            
        case 'defense':
            docContent = `民事答辩状

答辩人（被告）：${defendant}
被答辩人（原告）：${plaintiff}

因${cause}一案，现提出答辩如下：

答辩意见：
${facts}

综上所述，请求法院：
${requests}

此致
XXX 人民法院

答辩人：${defendant}
${today}
`;
            break;
            
        case 'agency':
            docContent = `代理词

审判长、审判员：

XXX 律师事务所接受${plaintiff}的委托，指派我担任其诉讼代理人。现根据事实和法律，发表如下代理意见：

一、案件基本情况
${facts}

二、法律分析
${requests}

三、代理意见
综上所述，恳请法院支持原告的全部诉讼请求。

此致
XXX 人民法院

代理人：XXX 律师
${today}
`;
            break;
            
        case 'lawyerLetter':
            docContent = `律师函

${defendant}：

XXX 律师事务所（以下简称"本所"）系根据中国法律登记注册的律师事务所。本所指派 XXX 律师（以下简称"本律师"）就${cause}一事，郑重致函如下：

一、事实概要
${facts}

二、法律分析
根据相关法律规定，${requests}

三、律师意见
请贵方在收到本函后 X 日内与本律师联系，妥善解决上述事宜。如逾期未予回应，本所将依委托人授权采取进一步法律措施。

特此函告！

XXX 律师事务所
XXX 律师
联系电话：XXX
${today}
`;
            break;
            
        case 'contract':
            docContent = `合 同 书

甲方：${plaintiff}
乙方：${defendant}

鉴于双方就${cause}事宜达成一致，特订立本合同：

第一条 合同内容
${facts}

第二条 双方权利义务
1. 甲方权利义务：
2. 乙方权利义务：

第三条 价款及支付方式

第四条 违约责任
${requests}

第五条 争议解决
本合同履行过程中发生争议，双方应协商解决；协商不成的，可向有管辖权的人民法院提起诉讼。

第六条 其他约定

甲方（签字）：__________    乙方（签字）：__________

签订日期：${today}
`;
            break;
            
        case 'power':
            docContent = `授权委托书

委托人：${plaintiff}
受托人：XXX 律师，XXX 律师事务所

现委托上列受托人在我与${defendant}${cause}一案中，作为我的诉讼代理人。

代理权限：
□ 一般代理
□ 特别授权（包括代为承认、放弃、变更诉讼请求，进行和解，提起反诉、上诉等）

委托期限：自本授权委托书签署之日起至本案审理终结止。

委托人（签字）：__________
${today}
`;
            break;
    }
    
    const resultDiv = document.getElementById('documentResult');
    resultDiv.style.display = 'block';
    document.getElementById('docContent').textContent = docContent;
    
    // 存储当前文档以便复制和下载
    window.currentDocument = docContent;
}

// 复制文书
function copyDocument() {
    if (window.currentDocument) {
        navigator.clipboard.writeText(window.currentDocument).then(() => {
            showNotification('文书已复制到剪贴板', 'success');
        });
    }
}

// 下载文书
function downloadDocument() {
    if (window.currentDocument) {
        const blob = new Blob([window.currentDocument], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `法律文书_${new Date().getTime()}.txt`;
        a.click();
        URL.revokeObjectURL(url);
        showNotification('文书已下载', 'success');
    }
}

/**
 * 法条检索（本地简易数据库）
 */
function searchLaw() {
    const keyword = document.getElementById('lawKeyword').value.trim();
    const category = document.getElementById('lawCategory').value;
    
    // 简易本地法条数据库
    const laws = [
        { category: 'civil', title: '《民法典》第 577 条', content: '当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。' },
        { category: 'civil', title: '《民法典》第 1165 条', content: '行为人因过错侵害他人民事权益造成损害的，应当承担侵权责任。' },
        { category: 'civil', title: '《民法典》第 1079 条', content: '夫妻一方要求离婚的，可以由有关组织进行调解或者直接向人民法院提起离婚诉讼。' },
        { category: 'civil', title: '《民法典》第 667 条', content: '借款合同是借款人向贷款人借款，到期返还借款并支付利息的合同。' },
        { category: 'labor', title: '《劳动合同法》第 38 条', content: '用人单位有下列情形之一的，劳动者可以解除劳动合同：（一）未按照劳动合同约定提供劳动保护或者劳动条件的；（二）未及时足额支付劳动报酬的...' },
        { category: 'labor', title: '《劳动合同法》第 47 条', content: '经济补偿按劳动者在本单位工作的年限，每满一年支付一个月工资的标准向劳动者支付。' },
        { category: 'criminal', title: '《刑法》第 264 条', content: '盗窃公私财物，数额较大的，或者多次盗窃、入户盗窃、携带凶器盗窃、扒窃的，处三年以下有期徒刑、拘役或者管制，并处或者单处罚金...' },
        { category: 'criminal', title: '《刑法》第 266 条', content: '诈骗公私财物，数额较大的，处三年以下有期徒刑、拘役或者管制，并处或者单处罚金...' },
        { category: 'procedure', title: '《民事诉讼法》第 122 条', content: '起诉必须符合下列条件：（一）原告是与本案有直接利害关系的公民、法人和其他组织；（二）有明确的被告；（三）有具体的诉讼请求和事实、理由；（四）属于人民法院受理民事诉讼的范围和受诉人民法院管辖。' },
        { category: 'company', title: '《公司法》第 3 条', content: '公司是企业法人，有独立的法人财产，享有法人财产权。公司以其全部财产对公司的债务承担责任。' },
    ];
    
    // 过滤搜索结果
    let results = laws;
    
    if (category !== 'all') {
        results = results.filter(law => law.category === category);
    }
    
    if (keyword) {
        results = results.filter(law => 
            law.title.includes(keyword) || 
            law.content.includes(keyword)
        );
    }
    
    // 显示结果
    const resultsDiv = document.getElementById('lawResults');
    if (results.length === 0) {
        resultsDiv.innerHTML = '<p style="text-align:center;color:#666;">未找到相关法条</p>';
    } else {
        resultsDiv.innerHTML = `
            <h4 style="margin-bottom:15px;">📚 找到 ${results.length} 条相关法条</h4>
            ${results.map(law => `
                <div style="background:#f8f9fa;padding:15px;border-radius:8px;margin-bottom:10px;border-left:4px solid #667eea;">
                    <strong style="color:#667eea;">${law.title}</strong>
                    <p style="margin-top:8px;color:#333;">${law.content}</p>
                </div>
            `).join('')}
            <p style="margin-top:20px;color:#666;font-size:0.9rem;">
                💡 提示：以上为部分常用法条，完整法条请查阅官方法律法规数据库。
            </p>
        `;
    }
}
