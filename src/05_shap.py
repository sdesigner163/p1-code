import lightgbm as lgb, shap, pandas as pd, os, yaml, matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')

cfg  = yaml.safe_load(open('config.yaml'))
model = lgb.Booster(model_file=f"{cfg['result_dir']}/model_0.txt")  # 例用第 0 折
dfs = [pd.read_parquet(f"{cfg['result_dir']}/{f}")
       for f in os.listdir(cfg['result_dir']) if f.startswith('pred_')]
X = pd.concat(dfs).sample(50000)[['rv','tr','vpin']]

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# 全局 summary
fig, ax = plt.subplots()
shap.summary_plot(shap_values, X, show=False)
plt.tight_layout()
fig.savefig(f"{cfg['result_dir']}/fig2_shap_summary.pdf")

# 交互
fig, ax = plt.subplots()
shap.dependence_plot('tr', shap_values, X, interaction_index='vpin', show=False)
plt.tight_layout()
fig.savefig(f"{cfg['result_dir']}/fig3_shap_interaction.pdf")