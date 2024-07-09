import streamlit as st


st.write(
"""

<style>
    h2 {
        border-bottom: 2px solid #eaecef;
        margin-bottom: 1em;

    }

    h3 {
        border-bottom: 1px solid #eaecef;
        margin-bottom: 1em;
    }
    
</style>


# DacQ-v2 のマニュアル 🦆📈

## DacQ-v2 とは?

DacQ-v2 は、 traP Kaggle班の部内データ分析コンペプラットフォームです！

DacQ-v2 は、チーム戦を含むコンペの開催、ディスカッション機能などを提供します。

## 使い方

DacQ の機能は大きく分けて二つのページで提供されます。

ひとつめは **home**、 ふたつめは **discussion** です。

### home

""", unsafe_allow_html=True
)


st.image("static/home.png")


st.write(
"""

home では

- 順位表の閲覧 (LeaderBoard)
- 予測の投稿 (Submit)
- データのダウンロード (Data)
- ルールの確認 (Rules)
- チーム設定 (Team Setting)

が行えます。

#### LeaderBoard

LeaderBoard では、現在の順位表を確認することができます。 Public / Private LB は自動で更新されます。

#### Submit

Submit では、予測ファイルを提出のチームの投稿履歴 (誰が投稿したか、いつ投稿したか) を確認できます。

#### Data

Data では、コンペで使用するデータをダウンロードすることができます。

#### Rules

Rules では、コンペのルールを確認することができます。

#### Team Setting

Team Setting では、チームの設定を行うことができます。
順位表に表示されるチーム名、チームのアイコンの設定ができます。



### discussion

"""
)


st.image("static/discussion.png")

st.write(
"""
discussion では、コンペに関する質問や情報共有を行うことができます。

投稿は、 Jupyter Notebook ファイル (.ipynb) をアップロードすることで行えます。

画像や Markdown のセルを含む Notebook もそのままアップロードが可能です。
"""
)