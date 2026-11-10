from pathlib import Path
import csv
import os
os.environ['MPLCONFIGDIR'] = '/tmp/pig_cycle_mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
from datetime import datetime

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)
font = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
bold = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
plt.rcParams.update({'axes.unicode_minus': False, 'pdf.fonttype': 42, 'svg.fonttype': 'path'})

sources = {
    '澎湃新闻': 'https://www.thepaper.cn/newsDetail_forward_16624811',
    '华安证券': 'https://finance.sina.com.cn/stock/relnews/cn/2026-03-10/doc-inhqneyw3404398.shtml',
    '国家发改委': 'https://www.ndrc.gov.cn/wsdwhfz/202107/t20210716_1290592.html',
    '农业部门监测': 'https://agri.hunan.gov.cn/agri/tslm/njnqx/202611/t20261103_34093452.html',
}
# Month-level positions are used for historical observations. They are selected
# reference points from multiple series, not a continuous monthly price series.
rows = [
    ('2016-05', 21.10, '阶段高点', '澎湃新闻', '2016年5月底'),
    ('2018-05', 9.90, '阶段低点', '澎湃新闻', '2018年5月上旬'),
    ('2019-10', 38.71, '阶段高点', '华安证券', '2019年10月30日'),
    ('2020-07', 37.80, '高位参考点', '国家发改委', '2020年7月中旬，约值'),
    ('2021-10', 11.54, '阶段低点', '华安证券', '2021年10月8日'),
    ('2022-10', 27.66, '阶段高点', '华安证券', '2022年10月26日'),
    ('2023-07', 14.19, '阶段低点', '华安证券', '2023年7月12日'),
    ('2024-08', 20.92, '阶段高点', '华安证券', '2024年8月15日'),
    ('2025-10', 12.30, '阶段低点', '华安证券', '2025年10月16日'),
    ('2026-10', 10.41, '近期周均价', '农业部门监测', '2026年10月26日至11月1日，全国活猪周均价'),
]
with (OUT/'pig_cycle_reference_points.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['展示月份','生猪价格_元每公斤','点位类型','来源','原始观测时间说明','来源链接'])
    for month, price, kind, source, note in rows:
        w.writerow([month, price, kind, source, note, sources[source]])

dates = [datetime.strptime(r[0]+'-15', '%Y-%m-%d') for r in rows]
dates[-1] = datetime(2026,10,29)
values = [r[1] for r in rows]
navy, muted, red, green, gold = '#172D45', '#62768A', '#C94747', '#218878', '#B3751D'
fig = plt.figure(figsize=(16,9), facecolor='#F6F8FB')
ax = fig.add_axes([.075,.25,.875,.54], facecolor='#FFFFFF')
fig.text(.075,.925,'近十年猪周期：一次超级上涨，随后多轮起落',fontproperties=bold,fontsize=25,color=navy)
fig.text(.075,.867,'2016—2026 中国生猪价格关键点  ·  单位：元/公斤（活猪，非猪肉零售价）',fontproperties=font,fontsize=13,color=muted)
fig.text(.95,.815,'● 历史代表价位    ◇ 近期周均价',fontproperties=font,fontsize=11,color=muted,ha='right')

ax.axvspan(datetime(2018,8,1),datetime(2020,12,31),color='#FFF1DF',alpha=.75,zorder=0)
ax.text(datetime(2019,9,1),45.3,'非洲猪瘟冲击后的高价阶段',ha='center',fontproperties=font,fontsize=12,color='#9E6524')
ax.plot(dates,values,color='#8A9BAA',linewidth=2,linestyle=(0,(4,4)),zorder=2)
for i,(d,y) in enumerate(zip(dates,values)):
    if i == len(rows)-1:
        ax.scatter([d],[y],s=120,marker='D',facecolors='white',edgecolors=gold,linewidths=2,zorder=4)
    else:
        c = green if '低点' in rows[i][2] else red
        ax.scatter([d],[y],s=72,c=c,edgecolors='white',linewidths=1.5,zorder=4)

offsets = [(0,16),(0,-43),(-19,7),(27,15),(0,-44),(0,16),(0,-45),(0,16),(-12,16),(0,-47)]
for i,((month,y,kind,source,note),(dx,dy)) in enumerate(zip(rows,offsets)):
    caption = f'{month}\n{y:.2f}'
    if i==9: caption='10/26—11/1 周均\n10.41'
    ax.annotate(caption,(dates[i],y),xytext=(dx,dy),textcoords='offset points',ha='center',va='bottom' if dy>0 else 'top',fontproperties=font,fontsize=11,color=navy,fontweight='normal')

ax.set_ylim(0,47)
ax.set_xlim(datetime(2015,11,1),datetime(2027,4,1))
ax.set_yticks([0,10,20,30,40])
ax.tick_params(axis='both',colors=muted,length=0,pad=10,labelsize=11)
ax.set_xticks([datetime(year,1,1) for year in range(2016,2027)])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.grid(axis='y',color='#E6EBF1',linewidth=.8)
for s in ax.spines.values(): s.set_visible(False)

fig.text(.075,.158,'2016见顶 → 2018探底 → 2019—2020高位 → 2021大跌 → 2022、2024反弹 → 近期再度承压',fontproperties=bold,fontsize=13,color=navy)
fig.text(.075,.109,'读图说明：虚线只连接所选观测点，不代表期间真实路径；未展示完整月度数据，也未预测未来价格。',fontproperties=font,fontsize=10,color=muted)
fig.text(.075,.077,'口径说明：历史点位来自不同公开监测资料；近期菱形点为全国活猪周均价，与历史点位并非完全同口径。',fontproperties=font,fontsize=10,color=muted)
fig.text(.075,.043,'来源：澎湃新闻、华安证券复盘、国家发改委、农业部门监测。整理日期：2026-11-10；详见配套数据说明。',fontproperties=font,fontsize=9,color=muted)
for ext in ['png','pdf','svg']:
    fig.savefig(OUT/f'pig_cycle_2016_2026.{ext}',dpi=180,facecolor=fig.get_facecolor())

notes = '''# 中国生猪价格关键点（2016—2026）

本图是对聊天中历史回顾的可视化，不是完整月度行情，也不是周期分界或未来价格预测。
历史日期按月份展示；CSV另列观测时间。虚线只连接选择的点位，不能据此推断两点之间的真实价格路径。
各资料监测口径不同，近期菱形点是全国活猪周均价，不能与历史日度价格作严格的同口径统计比较。
所有价格单位均为元/公斤，指生猪（活猪）价格，不是猪肉零售价格。
2020年7月中旬37.8元/公斤为原文约值。
资料整理日期：2026年11月10日。最近监测区间：2026年10月26日至11月1日。

## 来源
'''
for name,url in sources.items(): notes += f'\n- [{name}]({url})\n'
(OUT/'数据说明.md').write_text(notes,encoding='utf-8')
print(OUT/'pig_cycle_2016_2026.png')
