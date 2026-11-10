from pathlib import Path
import csv
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/gold_cycle_mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.ticker import StrMethodFormatter

OUT = Path(__file__).resolve().parent
HISTORY = 'https://www.goldprice.com/gold-price-history'
RECENT = 'https://www.reuters.com/world/india/gold-edges-lower-focus-shifts-us-inflation-data-2026-11-10/'

# year, annual high daily close/fix, annual low daily close/fix, year-end close.
# Transcribed from GoldPrice.com's yearly table, accessed 2026-11-10.
DATA = [
    (1996,414.80,367.40,369.25),
    (1997,366.55,283.00,290.20),
    (1998,313.15,273.40,287.80),
    (1999,325.50,252.80,290.25),
    (2000,312.70,263.80,274.45),
    (2001,293.25,255.95,276.50),
    (2002,349.30,277.75,347.20),
    (2003,416.25,319.90,416.25),
    (2004,454.20,375.00,435.60),
    (2005,536.50,411.10,513.00),
    (2006,725.00,524.75,632.00),
    (2007,841.10,608.40,833.75),
    (2008,1011.25,712.50,869.75),
    (2009,1212.50,810.00,1087.50),
    (2010,1421.00,1058.00,1405.50),
    (2011,1895.00,1319.00,1531.00),
    (2012,1791.75,1540.00,1657.50),
    (2013,1693.75,1192.00,1204.50),
    (2014,1385.00,1142.00,1206.00),
    (2015,1295.75,1049.40,1060.00),
    (2016,1366.25,1077.00,1145.90),
    (2017,1346.25,1151.00,1291.00),
    (2018,1354.95,1178.40,1279.00),
    (2019,1546.10,1269.50,1514.75),
    (2020,2067.15,1474.25,1887.60),
    (2021,1943.20,1683.95,1805.85),
    (2022,2039.05,1628.75,1813.75),
    (2023,2078.40,1810.95,2078.40),
    (2024,2777.80,1985.10,2609.10),
    (2025,4449.40,2633.35,4367.80),
    (2026,5405.00,3875.65,None),
]
LATEST = 4114.48  # Reuters, 2026-11-10 04:30 UTC = 12:30 Asia/Shanghai.

def write_data():
    with (OUT/'gold_annual_prices_1996_2026.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,lineterminator='\n')
        w.writerow(['year','high_daily_close_or_fix_usd_per_troy_oz','low_daily_close_or_fix_usd_per_troy_oz','year_end_close_usd_per_troy_oz','period_status','source_url'])
        for y,hi,lo,close in DATA:
            w.writerow([y,hi,lo,'' if close is None else close,'partial_year_as_available_2026-11-10' if y==2026 else 'completed_year',HISTORY])
    with (OUT/'gold_recent_quote.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,lineterminator='\n')
        w.writerow(['time_utc','time_asia_shanghai','price_usd_per_troy_oz','price_type','source_url'])
        w.writerow(['2026-11-10T04:30:00Z','2026-11-10T12:30:00+08:00',LATEST,'spot_quote_not_year_end_close',RECENT])

def draw():
    font=FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
    bold=FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    plt.rcParams.update({'axes.unicode_minus':False,'pdf.fonttype':42,'svg.fonttype':'path'})
    ink='#192E43'; muted='#65788C'; gold='#AC7A20'; gray='#9AA7B5'
    fig=plt.figure(figsize=(16,10),facecolor='#F6F8FB')
    fig.text(.075,.93,'近30年金价：长期上涨中的多轮回撤',fontproperties=bold,fontsize=26,color=ink)
    fig.text(.075,.88,'1996—2026  ·  国际黄金  ·  名义美元 / 金衡盎司  ·  未作通胀调整',fontproperties=font,fontsize=13,color=muted)
    ax=fig.add_axes([.075,.325,.86,.455],facecolor='white')
    phases=[
        (1995.5,2001.5,'#EDF2F7'),
        (2001.5,2011.5,'#FFF3D9'),
        (2011.5,2015.5,'#E8F3EF'),
        (2015.5,2022.5,'#EDF2F7'),
        (2022.5,2026.5,'#FFF3D9'),
    ]
    for a,b,c in phases: ax.axvspan(a,b,color=c,alpha=.75,zorder=0)
    years=[r[0] for r in DATA]; highs=[r[1] for r in DATA]; lows=[r[2] for r in DATA]
    ax.vlines(years,lows,highs,color=gray,lw=2.2,alpha=.75,zorder=2)
    ax.hlines(highs,[y-.11 for y in years],[y+.11 for y in years],color=gray,lw=1.1,zorder=2)
    ax.hlines(lows,[y-.11 for y in years],[y+.11 for y in years],color=gray,lw=1.1,zorder=2)
    ax.plot(years[:-1],[r[3] for r in DATA[:-1]],color=gold,lw=2.6,marker='o',ms=4,zorder=4)
    ax.plot([2025,2026],[DATA[-2][3],LATEST],color=gold,lw=2,ls=(0,(4,3)),zorder=3)
    ax.scatter([2026],[LATEST],marker='D',s=75,facecolors='white',edgecolors=gold,lw=2,zorder=5)
    ax.scatter([2026],[5405],marker='*',s=125,color=gold,edgecolors='white',lw=.6,zorder=5)

    def label(x,y,text,dx,dy,ha='center'):
        ax.annotate(text,(x,y),xytext=(dx,dy),textcoords='offset points',ha=ha,va='bottom' if dy>0 else 'top',fontproperties=font,fontsize=11,color=ink,arrowprops={'arrowstyle':'-','color':gray,'lw':.8},bbox={'boxstyle':'round,pad=.25','facecolor':'white','edgecolor':'none','alpha':.92},zorder=8)
    label(1999,252.8,'1999 年内低点\n253',0,28)
    label(2011,1895,'2011 年内高点\n1,895',-12,30)
    label(2015,1049.4,'2015 年内低点\n1,049',0,-32)
    label(2020,2067.15,'2020 年内高点\n2,067',-15,28)
    label(2025,4367.8,'2025 年末\n4,368',-60,8)
    label(2026,5405,'2026-01-29 日收盘高点\n5,405',-75,20)
    label(2026,LATEST,'11月10日现货\n4,114',30,-30,ha='left')
    ax.set_xlim(1995.5,2028.2); ax.set_ylim(0,6350)
    ax.set_xticks([1996,2001,2006,2011,2016,2021,2026])
    ax.set_yticks([0,1000,2000,3000,4000,5000,6000])
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax.tick_params(axis='both',length=0,pad=10,labelsize=11,colors=muted)
    ax.grid(axis='y',color='#E0E6ED',lw=.8)
    for s in ax.spines.values(): s.set_visible(False)
    handles=[Line2D([0],[0],color=gold,lw=2.5,marker='o',ms=4),Line2D([0],[0],color=gray,lw=2),Line2D([0],[0],color=gold,lw=0,marker='D',mfc='white',ms=6)]
    ax.legend(handles,['1996—2025 年末价','年度日收盘 / 定盘价高低区间','2026 近期现货报价'],loc='upper left',bbox_to_anchor=(0,1.14),ncol=3,frameon=False,prop=font,labelcolor=muted,handlelength=2,columnspacing=2)

    cards=[
        ('1996—2001','低位徘徊','#EDF2F7'),
        ('2002—2011','长期上涨','#FFF3D9'),
        ('2012—2015','调整回落','#E8F3EF'),
        ('2016—2022','震荡抬升','#EDF2F7'),
        ('2023—2026','上涨后回撤','#FFF3D9'),
    ]
    fig.text(.075,.252,'阶段概括',fontproperties=bold,fontsize=12,color=ink)
    for i,(date,txt,c) in enumerate(cards):
        x=.075+i*.174
        fig.patches.append(plt.Rectangle((x,.158),.162,.075,transform=fig.transFigure,facecolor=c,edgecolor='none',zorder=1))
        fig.text(x+.012,.206,date,fontproperties=font,fontsize=11,color=muted)
        fig.text(x+.012,.174,txt,fontproperties=bold,fontsize=14,color=ink)
    fig.text(.075,.113,'读图：金线为年末价，灰线保留年内波动；2026年尚未结束，菱形是11月10日12:30（北京时间）的现货报价。',fontproperties=font,fontsize=10,color=muted)
    fig.text(.075,.080,'口径：历史表2015年前为LBMA定盘价，其后为Metals.dev日收盘；近期为路透现货。阶段为走势概括，不表示固定周期。',fontproperties=font,fontsize=10,color=muted)
    fig.text(.075,.047,'来源：GoldPrice.com 历年汇总、Reuters 2026-11-10 报道。年度点间连线不代表完整日内路径；详见配套CSV及来源说明。',fontproperties=font,fontsize=9,color=muted)
    for ext in ['png','pdf','svg']:
        fig.savefig(OUT/f'gold_cycle_1996_2026.{ext}',dpi=180,facecolor=fig.get_facecolor())

def write_readme():
    text=f'''# 近30年国际金价周期图（1996—2026）

![金价周期图](gold_cycle_1996_2026.png)

## 图表口径

- 单位：名义美元/金衡盎司，未作通胀调整，不是人民币金价或金店首饰售价。
- 1996—2025年金色折线：逐年年末最后一笔收盘价；灰色竖线：该年日收盘/定盘价序列的高低区间，不是盘中最高最低价。
- 历史汇总表说明：2015年之前使用LBMA定盘价，之后接续Metals.dev日收盘价，历史口径存在变更。
- 2026年灰线为来源页面查询时已提供的年内区间，不能视为全年数据。2026年年末收盘价留空，没有预测或填造。
- 2026年菱形：Reuters报道的2026年11月10日04:30 UTC（北京时间12:30）国际现货报价4,114.48美元/盎司，与历史收盘序列口径有差别。
- 2026年1月29日5,405美元为GoldPrice.com序列内的日收盘高点，不是盘中历史最高成交价。
- 年份横轴用于年度汇总；连线不代表两点之间的实际每日行情。
- 阶段文字是作者为便于读图作的概括，不是官方周期划分，也不表示黄金有固定长度的周期。

## 数据来源

1. [GoldPrice.com 历年黄金价格汇总]({HISTORY})：1996—2025年年末价、1996—2026年日收盘/定盘价年度高低值，以及2026年1月29日日收盘高点。查询日期：2026年11月10日。
2. [Reuters：Gold edges lower as focus shifts to US inflation data]({RECENT})：2026年11月10日04:30 UTC现货报价，来自该报道的检索摘要。

## 文件与复现

- `gold_annual_prices_1996_2026.csv`：年度价格数据，2026年标为partial_year，year_end_close留空。
- `gold_recent_quote.csv`：近期报价和精确时点。
- `gold_cycle_1996_2026.png` / `.pdf` / `.svg`：图表导出文件。
- `draw_gold_cycle.py`：生成图表与CSV。依赖Python、matplotlib及Noto Sans CJK字体；其他系统请调整脚本内的字体路径。

```bash
python draw_gold_cycle.py
```

数据为公开来源的转录汇总，整理日期：2026年11月10日。
'''
    (OUT/'README.md').write_text(text,encoding='utf-8')

if __name__=='__main__':
    assert [r[0] for r in DATA] == list(range(1996,2027))
    assert all(lo<=hi and (close is None or lo<=close<=hi) for _,hi,lo,close in DATA)
    write_data(); draw(); write_readme()
    print(OUT/'gold_cycle_1996_2026.png')
