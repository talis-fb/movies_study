"""
Análise Completa dos Clusters de Filmes
=======================================

Este script analisa o dataset dataset_com_cluster.csv que contém filmes categorizados 
em clusters baseados em características como orçamento, popularidade, duração, 
avaliações do IMDB e Rotten Tomatoes.

Clusters Identificados:
- ACAO_DE_PAI: 265 filmes
- ACAO_FANTASIA: 228 filmes  
- ACAO_REALISTA: 178 filmes
- DRAMAS: 479 filmes
- FAMILIA: 169 filmes
- ROMANCES: 222 filmes
- THRILLER: 264 filmes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
from datetime import datetime
import os

# Configurações
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Configurar para salvar gráficos
os.makedirs('cluster_analysis_output', exist_ok=True)

def load_and_clean_data():
    """Carrega e limpa o dataset"""
    print("Carregando dataset...")
    df = pd.read_csv('dataset_com_cluster.csv')
    
    # Removendo a linha de cabeçalho duplicada
    df = df[df['cluster'] != 'cluster'].copy()
    
    # Convertendo colunas numéricas
    numeric_columns = ['budget', 'popularity', 'revenue', 'runtime', 'Metacritic', 'imdb', 'rotten']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Calculando métricas financeiras
    df['profit'] = df['revenue'] - df['budget']
    df['roi'] = (df['profit'] / df['budget']) * 100
    
    # Convertendo ano
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    print(f"Dataset carregado com {len(df)} filmes")
    return df

def analyze_cluster_distribution(df):
    """Analisa a distribuição dos clusters"""
    print("\n=== ANÁLISE DA DISTRIBUIÇÃO DOS CLUSTERS ===")
    
    cluster_counts = df['cluster'].value_counts()
    
    # Gráfico de distribuição
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(cluster_counts)))
    bars = ax1.bar(cluster_counts.index, cluster_counts.values, color=colors)
    ax1.set_title('Distribuição dos Clusters', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Clusters')
    ax1.set_ylabel('Número de Filmes')
    ax1.tick_params(axis='x', rotation=45)
    
    for bar, count in zip(bars, cluster_counts.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                 str(count), ha='center', va='bottom', fontweight='bold')
    
    ax2.pie(cluster_counts.values, labels=cluster_counts.index, autopct='%1.1f%%', 
            colors=colors, startangle=90)
    ax2.set_title('Proporção dos Clusters', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('cluster_analysis_output/01_cluster_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nDistribuição detalhada:")
    for cluster, count in cluster_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{cluster}: {count} filmes ({percentage:.1f}%)")
    
    return cluster_counts

def analyze_financial_performance(df):
    """Analisa performance financeira por cluster"""
    print("\n=== ANÁLISE DE PERFORMANCE FINANCEIRA ===")
    
    financial_metrics = ['budget', 'revenue', 'profit', 'roi']
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Orçamento médio por cluster
    budget_means = df.groupby('cluster')['budget'].mean() / 1e6
    axes[0,0].bar(budget_means.index, budget_means.values, color='skyblue')
    axes[0,0].set_title('Orçamento Médio por Cluster (Milhões $)')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2. Receita média por cluster
    revenue_means = df.groupby('cluster')['revenue'].mean() / 1e6
    axes[0,1].bar(revenue_means.index, revenue_means.values, color='lightgreen')
    axes[0,1].set_title('Receita Média por Cluster (Milhões $)')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # 3. Lucro médio por cluster
    profit_means = df.groupby('cluster')['profit'].mean() / 1e6
    colors = ['red' if x < 0 else 'green' for x in profit_means.values]
    axes[1,0].bar(profit_means.index, profit_means.values, color=colors)
    axes[1,0].set_title('Lucro Médio por Cluster (Milhões $)')
    axes[1,0].tick_params(axis='x', rotation=45)
    axes[1,0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # 4. ROI médio por cluster
    roi_means = df.groupby('cluster')['roi'].mean()
    colors = ['red' if x < 0 else 'green' for x in roi_means.values]
    axes[1,1].bar(roi_means.index, roi_means.values, color=colors)
    axes[1,1].set_title('ROI Médio por Cluster (%)')
    axes[1,1].tick_params(axis='x', rotation=45)
    axes[1,1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('cluster_analysis_output/02_financial_performance.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Tabela resumo financeiro
    financial_summary = df.groupby('cluster').agg({
        'budget': ['mean', 'median'],
        'revenue': ['mean', 'median'],
        'profit': ['mean', 'median'],
        'roi': ['mean', 'median']
    }).round(2)
    
    print("\nResumo Financeiro por Cluster:")
    print(financial_summary)
    
    return financial_summary

def analyze_quality_ratings(df):
    """Analisa avaliações de qualidade por cluster"""
    print("\n=== ANÁLISE DE QUALIDADE E AVALIAÇÕES ===")
    
    quality_metrics = ['imdb', 'rotten', 'Metacritic']
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for i, metric in enumerate(quality_metrics):
        if metric in df.columns:
            sns.boxplot(data=df, x='cluster', y=metric, ax=axes[i])
            axes[i].set_title(f'{metric.upper()} por Cluster')
            axes[i].tick_params(axis='x', rotation=45)
            
            means = df.groupby('cluster')[metric].mean()
            for j, (cluster, mean_val) in enumerate(means.items()):
                if not pd.isna(mean_val):
                    axes[i].text(j, mean_val, f'{mean_val:.1f}', 
                                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('cluster_analysis_output/03_quality_ratings.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Correlação entre avaliações e performance financeira
    correlation_metrics = ['imdb', 'rotten', 'profit', 'roi']
    correlation_data = df[correlation_metrics].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5)
    plt.title('Correlação entre Avaliações e Performance Financeira')
    plt.savefig('cluster_analysis_output/04_correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return correlation_data

def analyze_success_rates(df):
    """Analisa taxas de sucesso por cluster"""
    print("\n=== ANÁLISE DE TAXAS DE SUCESSO ===")
    
    # Definindo critérios de sucesso
    df['financial_success'] = df['profit'] > 0
    df['critical_success'] = (df['imdb'] > 7.0) & (df['rotten'] > 70)
    df['popular_success'] = df['popularity'] > df['popularity'].median()
    
    success_metrics = ['financial_success', 'critical_success', 'popular_success']
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for i, metric in enumerate(success_metrics):
        success_rate = df.groupby('cluster')[metric].mean() * 100
        
        colors = plt.cm.RdYlGn(success_rate / 100)
        bars = axes[i].bar(success_rate.index, success_rate.values, color=colors)
        axes[i].set_title(f'Taxa de Sucesso: {metric.replace("_", " ").title()}')
        axes[i].set_ylabel('Taxa de Sucesso (%)')
        axes[i].tick_params(axis='x', rotation=45)
        
        for bar, rate in zip(bars, success_rate.values):
            axes[i].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                         f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('cluster_analysis_output/05_success_rates.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Tabela resumo de sucesso
    success_summary = df.groupby('cluster').agg({
        'financial_success': 'mean',
        'critical_success': 'mean',
        'popular_success': 'mean'
    }).round(3) * 100
    
    print("\nTaxa de Sucesso por Cluster (%):")
    print(success_summary)
    
    return success_summary

def analyze_temporal_trends(df):
    """Analisa tendências temporais por cluster"""
    print("\n=== ANÁLISE DE TENDÊNCIAS TEMPORAIS ===")
    
    # Distribuição por ano
    yearly_distribution = df.groupby(['Year', 'cluster']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(15, 8))
    yearly_distribution.plot(kind='line', marker='o', linewidth=2, markersize=6)
    plt.title('Evolução dos Clusters ao Longo do Tempo', fontsize=16, fontweight='bold')
    plt.xlabel('Ano')
    plt.ylabel('Número de Filmes')
    plt.legend(title='Clusters', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('cluster_analysis_output/06_temporal_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Performance financeira por ano
    yearly_performance = df.groupby(['Year', 'cluster'])['profit'].mean().unstack()
    
    plt.figure(figsize=(15, 8))
    yearly_performance.plot(kind='line', marker='o', linewidth=2, markersize=6)
    plt.title('Lucro Médio por Cluster ao Longo do Tempo', fontsize=16, fontweight='bold')
    plt.xlabel('Ano')
    plt.ylabel('Lucro Médio (Milhões $)')
    plt.legend(title='Clusters', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('cluster_analysis_output/07_temporal_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

def analyze_genres(df):
    """Analisa gêneros por cluster"""
    print("\n=== ANÁLISE DE GÊNEROS ===")
    
    def extract_genres(genre_str):
        if pd.isna(genre_str):
            return []
        try:
            genres = genre_str.replace("['", '').replace("']", '').split("', '")
            return [g.strip() for g in genres]
        except:
            return []
    
    df['genres_list'] = df['genres'].apply(extract_genres)
    
    # Criando lista de todos os gêneros
    all_genres = []
    for genres in df['genres_list']:
        all_genres.extend(genres)
    
    genre_counts = pd.Series(all_genres).value_counts().head(15)
    
    plt.figure(figsize=(12, 8))
    genre_counts.plot(kind='bar', color='lightcoral')
    plt.title('Top 15 Gêneros Mais Frequentes', fontsize=16, fontweight='bold')
    plt.xlabel('Gênero')
    plt.ylabel('Frequência')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('cluster_analysis_output/08_top_genres.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Análise de gêneros por cluster
    cluster_genres = {}
    for cluster in df['cluster'].unique():
        cluster_data = df[df['cluster'] == cluster]
        cluster_all_genres = []
        for genres in cluster_data['genres_list']:
            cluster_all_genres.extend(genres)
        cluster_genres[cluster] = pd.Series(cluster_all_genres).value_counts().head(5)
    
    print("\nTop 5 Gêneros por Cluster:")
    for cluster, genres in cluster_genres.items():
        print(f"\n{cluster}:")
        for genre, count in genres.items():
            print(f"  {genre}: {count}")

def generate_executive_summary(df):
    """Gera resumo executivo com insights principais"""
    print("\n" + "=" * 80)
    print("RESUMO EXECUTIVO - ANÁLISE DOS CLUSTERS DE FILMES")
    print("=" * 80)
    
    # 1. Clusters mais lucrativos
    most_profitable = df.groupby('cluster')['profit'].mean().sort_values(ascending=False)
    print(f"\n1. CLUSTERS MAIS LUCRATIVOS (Lucro Médio):")
    for cluster, profit in most_profitable.items():
        print(f"   {cluster}: ${profit/1e6:.1f}M")
    
    # 2. Clusters com melhor ROI
    best_roi = df.groupby('cluster')['roi'].mean().sort_values(ascending=False)
    print(f"\n2. CLUSTERS COM MELHOR ROI:")
    for cluster, roi in best_roi.items():
        print(f"   {cluster}: {roi:.1f}%")
    
    # 3. Clusters com melhores avaliações
    best_ratings = df.groupby('cluster')['imdb'].mean().sort_values(ascending=False)
    print(f"\n3. CLUSTERS COM MELHORES AVALIAÇÕES (IMDB):")
    for cluster, rating in best_ratings.items():
        print(f"   {cluster}: {rating:.1f}/10")
    
    # 4. Clusters com maior taxa de sucesso financeiro
    success_rate = df.groupby('cluster')['financial_success'].mean().sort_values(ascending=False)
    print(f"\n4. TAXA DE SUCESSO FINANCEIRO:")
    for cluster, rate in success_rate.items():
        print(f"   {cluster}: {rate*100:.1f}%")
    
    # 5. Análise de risco
    risk_analysis = df.groupby('cluster').agg({
        'profit': ['mean', 'std'],
        'roi': ['mean', 'std']
    }).round(2)
    
    print(f"\n5. ANÁLISE DE RISCO (Média ± Desvio Padrão):")
    for cluster in df['cluster'].unique():
        profit_mean = risk_analysis.loc[cluster, ('profit', 'mean')] / 1e6
        profit_std = risk_analysis.loc[cluster, ('profit', 'std')] / 1e6
        roi_mean = risk_analysis.loc[cluster, ('roi', 'mean')]
        roi_std = risk_analysis.loc[cluster, ('roi', 'std')]
        
        print(f"   {cluster}: Lucro ${profit_mean:.1f}M ± ${profit_std:.1f}M, ROI {roi_mean:.1f}% ± {roi_std:.1f}%")
    
    print("\n" + "=" * 80)
    print("RECOMENDAÇÕES ESTRATÉGICAS:")
    print("=" * 80)
    
    recommendations = {
        'ACAO_DE_PAI': 'Alto risco, alto retorno. Investir em filmes com orçamento moderado e foco em qualidade.',
        'ACAO_FANTASIA': 'Bom potencial de lucro. Priorizar efeitos especiais e narrativas envolventes.',
        'ACAO_REALISTA': 'Estável e previsível. Bom para investimentos conservadores.',
        'DRAMAS': 'Maior volume, variabilidade média. Focar em roteiros de qualidade e direção artística.',
        'FAMILIA': 'Baixo risco, retorno consistente. Ideal para investimentos de longo prazo.',
        'ROMANCES': 'Mercado nicho estável. Investir em elencos atrativos e marketing direcionado.',
        'THRILLER': 'Alta competição, mas bom potencial. Focar em originalidade e tensão narrativa.'
    }
    
    for cluster, recommendation in recommendations.items():
        print(f"\n{cluster}: {recommendation}")
    
    print("\n" + "=" * 80)

def save_detailed_analysis(df):
    """Salva análise detalhada em arquivo CSV"""
    print("\n=== SALVANDO ANÁLISE DETALHADA ===")
    
    # Estatísticas por cluster
    cluster_stats = df.groupby('cluster').agg({
        'budget': ['count', 'mean', 'median', 'std'],
        'revenue': ['mean', 'median', 'std'],
        'profit': ['mean', 'median', 'std'],
        'roi': ['mean', 'median', 'std'],
        'popularity': ['mean', 'median', 'std'],
        'runtime': ['mean', 'median', 'std'],
        'imdb': ['mean', 'median', 'std'],
        'rotten': ['mean', 'median', 'std']
    }).round(2)
    
    # Taxas de sucesso
    df['financial_success'] = df['profit'] > 0
    df['critical_success'] = (df['imdb'] > 7.0) & (df['rotten'] > 70)
    df['popular_success'] = df['popularity'] > df['popularity'].median()
    
    success_stats = df.groupby('cluster').agg({
        'financial_success': 'mean',
        'critical_success': 'mean',
        'popular_success': 'mean'
    }).round(3) * 100
    
    # Combinando estatísticas
    detailed_analysis = pd.concat([cluster_stats, success_stats], axis=1)
    detailed_analysis.to_csv('cluster_analysis_output/detailed_cluster_analysis.csv')
    
    print("Análise detalhada salva em 'cluster_analysis_output/detailed_cluster_analysis.csv'")

def main():
    """Função principal que executa toda a análise"""
    print("INICIANDO ANÁLISE DOS CLUSTERS DE FILMES")
    print("=" * 50)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Carregar dados
    df = load_and_clean_data()
    
    # Executar análises
    cluster_dist = analyze_cluster_distribution(df)
    financial_summary = analyze_financial_performance(df)
    correlation_data = analyze_quality_ratings(df)
    success_summary = analyze_success_rates(df)
    analyze_temporal_trends(df)
    analyze_genres(df)
    
    # Gerar resumo executivo
    generate_executive_summary(df)
    
    # Salvar análise detalhada
    save_detailed_analysis(df)
    
    print("\n" + "=" * 50)
    print("ANÁLISE CONCLUÍDA!")
    print("Gráficos salvos na pasta 'cluster_analysis_output/'")
    print("=" * 50)

if __name__ == "__main__":
    main() 