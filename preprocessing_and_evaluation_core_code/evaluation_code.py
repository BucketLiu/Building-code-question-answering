import pandas as pd
from bert_score import score
from bert_score.utils import model2layers
import os
from rouge_chinese import Rouge  # 使用专门处理中文的ROUGE库
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import jieba
import re
import logging
from tqdm import tqdm  # 添加进度条

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. 设置本地模型路径
model_path = r"bert-base-multilingual-cased"
model2layers[model_path] = 12  # 手动注册层数，确保BERT模型正确加载

# 2. 文件路径处理
input_file = r"input_data.xlsx"  # 替换为你的输入文件路径
output_file = os.path.splitext(input_file)[0] + "_scores.xlsx"

# 3. 初始化评估工具
rouge = Rouge(
    metrics=['rouge-1', 'rouge-2', 'rouge-l'],
)
smoother = SmoothingFunction().method1

# 中文标点符号集合
chinese_punctuation = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."


def preprocess_text(text):
    """增强版中文文本预处理"""
    if not isinstance(text, str):
        return ""

    # 基础清洗
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text.strip())
    text = re.sub(r'\s+', ' ', text)

    # 精确模式分词+过滤
    words = jieba.lcut(text)
    words = [w for w in words if w.strip() and w not in chinese_punctuation]

    return ' '.join(words)


# 4. 读取Excel文件
try:
    df = pd.read_excel(input_file)
    logger.info(f"成功读取文件: {input_file}，共{len(df)}条数据")
except Exception as e:
    logger.error(f"文件读取失败: {str(e)}")
    raise

# 5. 预处理列数据
ref_col = df.columns[1]  # 第二列作为参考
pred_col = df.columns[2]  # 第三列作为预测

# 在计算时使用分词后的文本，但不改变原始文本
df['ref_processed'] = df[ref_col].astype(str).apply(preprocess_text)
df['pred_processed'] = df[pred_col].astype(str).apply(preprocess_text)

# 6. 分批处理
batch_size = 20
bert_results = []
rouge_results = []
bleu_results = []

for i in tqdm(range(0, len(df), batch_size), desc="处理进度"):
    batch_refs = df['ref_processed'].iloc[i:i + batch_size].tolist()
    batch_preds = df['pred_processed'].iloc[i:i + batch_size].tolist()

    # BERTScore计算
    try:
        P, R, F1 = score(
            batch_preds,
            batch_refs,
            lang="zh",
            model_type=model_path,
            use_fast_tokenizer=True,
            verbose=False
        )
        bert_results.extend(zip(P.tolist(), R.tolist(), F1.tolist()))
    except Exception as e:
        logger.warning(f"BERTScore计算异常: {str(e)}")
        bert_results.extend([(0, 0, 0)] * len(batch_refs))

    # ROUGE和BLEU计算
    for ref, pred in zip(batch_refs, batch_preds):
        # ROUGE计算
        rouge_score = {'rouge-1': 0, 'rouge-2': 0, 'rouge-l': 0}
        if ref and pred:
            try:
                scores = rouge.get_scores(pred, ref)
                if scores:
                    rouge_score = {
                        'rouge-1': scores[0]['rouge-1']['f'],
                        'rouge-2': scores[0]['rouge-2']['f'],
                        'rouge-l': scores[0]['rouge-l']['f']
                    }
            except Exception as e:
                logger.debug(f"ROUGE计算异常: {str(e)}")
        rouge_results.append(rouge_score)

        # BLEU计算
        bleu_score = 0
        if ref and pred:
            try:
                ref_tokens = ref.split()
                pred_tokens = pred.split()
                if len(ref_tokens) >= 4:  # 足够长的文本才计算BLEU
                    bleu_score = sentence_bleu(
                        [ref_tokens],
                        pred_tokens,
                        weights=(0.25, 0.25, 0.25, 0.25),
                        smoothing_function=smoother
                    )
            except Exception as e:
                logger.debug(f"BLEU计算异常: {str(e)}")
        bleu_results.append(bleu_score)

# 7. 添加结果列
df["BERTScore_P"] = [r[0] for r in bert_results]
df["BERTScore_R"] = [r[1] for r in bert_results]
df["BERTScore_F1"] = [r[2] for r in bert_results]

df["ROUGE-1"] = [r['rouge-1'] for r in rouge_results]
df["ROUGE-2"] = [r['rouge-2'] for r in rouge_results]
df["ROUGE-L"] = [r['rouge-l'] for r in rouge_results]

df["BLEU"] = bleu_results

# 8. 添加统计信息
stats_df = pd.DataFrame({
    "指标": ["平均值", "中位数", "最大值", "最小值", "非零比例"],
    "BERTScore_P": [
        df["BERTScore_P"].mean(),
        df["BERTScore_P"].median(),
        df["BERTScore_P"].max(),
        df["BERTScore_P"].min(),
        (df["BERTScore_P"] > 0).mean()
    ],
    "BERTScore_R": [
        df["BERTScore_R"].mean(),
        df["BERTScore_R"].median(),
        df["BERTScore_R"].max(),
        df["BERTScore_R"].min(),
        (df["BERTScore_R"] > 0).mean()
    ],
    "BERTScore_F1": [
        df["BERTScore_F1"].mean(),
        df["BERTScore_F1"].median(),
        df["BERTScore_F1"].max(),
        df["BERTScore_F1"].min(),
        (df["BERTScore_F1"] > 0).mean()
    ],
    "ROUGE-1": [
        df["ROUGE-1"].mean(),
        df["ROUGE-1"].median(),
        df["ROUGE-1"].max(),
        df["ROUGE-1"].min(),
        (df["ROUGE-1"] > 0).mean()
    ],
    "ROUGE-2": [
        df["ROUGE-2"].mean(),
        df["ROUGE-2"].median(),
        df["ROUGE-2"].max(),
        df["ROUGE-2"].min(),
        (df["ROUGE-2"] > 0).mean()
    ],
    "ROUGE-L": [
        df["ROUGE-L"].mean(),
        df["ROUGE-L"].median(),
        df["ROUGE-L"].max(),
        df["ROUGE-L"].min(),
        (df["ROUGE-L"] > 0).mean()
    ],
    "BLEU": [
        df["BLEU"].mean(),
        df["BLEU"].median(),
        df["BLEU"].max(),
        df["BLEU"].min(),
        (df["BLEU"] > 0).mean()
    ]
})

# 9. 保存结果
try:
    with pd.ExcelWriter(output_file) as writer:
        df.to_excel(writer, sheet_name="详细结果", index=False)  # 原始列保留
        stats_df.to_excel(writer, sheet_name="统计信息", index=False)
    logger.info(f"结果已保存到: {output_file}")
except Exception as e:
    logger.error(f"文件保存失败: {str(e)}")
    raise

# 打印关键统计信息
print("\n关键指标统计:")
print(f"ROUGE-1 平均值: {df['ROUGE-1'].mean():.4f} (非零比例: {(df['ROUGE-1'] > 0).mean():.1%})")
print(f"ROUGE-2 平均值: {df['ROUGE-2'].mean():.4f} (非零比例: {(df['ROUGE-2'] > 0).mean():.1%})")
print(f"ROUGE-L 平均值: {df['ROUGE-L'].mean():.4f} (非零比例: {(df['ROUGE-L'] > 0).mean():.1%})")
print(f"BLEU 平均值: {df['BLEU'].mean():.4f} (非零比例: {(df['BLEU'] > 0).mean():.1%})")
