#!/usr/bin/env python3
"""
Criação de Gráficos para Análise dos Clusters de Filmes
=======================================================

Este script cria visualizações dos dados analisados do dataset_com_cluster.csv
"""

import csv
from collections import defaultdict
import statistics
import os

def load_data():
    """Carrega o dataset CSV"""
    print("Carregando dataset_com_cluster.csv...")
    
    data = []
    with open('dataset_com_cluster.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['cluster'] == 'cluster':
                continue
            data.append(row)
    
    print(f"Dataset carregado com {len(data)} filmes")
    return data

def convert_to_numeric(value):
    """Converte string para número, retorna None se não conseguir"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def create_text_charts(data):
    """Cria gráficos em texto ASCII"""
    print("\n" + "="*80)
    print("GRÁFICOS EM TEXTO ASCII")
    print("="*80)
    
    # 1. Distribuição dos Clusters (Gráfico de barras em texto)
    print("\n1. DISTRIBUIÇÃO DOS CLUSTERS")
    print("-" * 50)
    
    cluster_counts = defaultdict(int)
    for row in data:
        cluster_counts[row['cluster']] += 1
    
    total = len(data)
    max_count = max(cluster_counts.values())
    max_bar_length = 40
    
    for cluster, count in sorted(cluster_counts.items()):
        percentage = (count / total) * 100
        bar_length = int((count / max_count) * max_bar_length)
        bar = "█" * bar_length
        print(f"{cluster:15} | {bar} {count:4d} ({percentage:5.1f}%)")
    
    # 2. Performance Financeira (Gráfico de barras)
    print("\n\n2. LUCRO MÉDIO POR CLUSTER (Milhões $)")
    print("-" * 50)
    
    cluster_profits = defaultdict(list)
    for row in data:
        cluster = row['cluster']
        budget = convert_to_numeric(row['budget'])
        revenue = convert_to_numeric(row['revenue'])
        if budget and revenue and budget > 0:
            profit = revenue - budget
            cluster_profits[cluster].append(profit)
    
    avg_profits = {}
    for cluster, profits in cluster_profits.items():
        if profits:
            avg_profits[cluster] = statistics.mean(profits) / 1e6
    
    max_profit = max(avg_profits.values()) if avg_profits else 1
    max_bar_length = 30
    
    for cluster, avg_profit in sorted(avg_profits.items(), key=lambda x: x[1], reverse=True):
        bar_length = int((avg_profit / max_profit) * max_bar_length)
        bar = "█" * bar_length
        color = "🟢" if avg_profit > 0 else "🔴"
        print(f"{cluster:15} | {bar} ${avg_profit:6.1f}M {color}")
    
    # 3. Avaliações IMDB (Gráfico de barras)
    print("\n\n3. AVALIAÇÕES IMDB MÉDIAS POR CLUSTER")
    print("-" * 50)
    
    cluster_imdb = defaultdict(list)
    for row in data:
        cluster = row['cluster']
        imdb = convert_to_numeric(row['imdb'])
        if imdb:
            cluster_imdb[cluster].append(imdb)
    
    avg_imdb = {}
    for cluster, ratings in cluster_imdb.items():
        if ratings:
            avg_imdb[cluster] = statistics.mean(ratings)
    
    max_rating = max(avg_imdb.values()) if avg_imdb else 10
    max_bar_length = 25
    
    for cluster, rating in sorted(avg_imdb.items(), key=lambda x: x[1], reverse=True):
        bar_length = int((rating / max_rating) * max_bar_length)
        bar = "█" * bar_length
        print(f"{cluster:15} | {bar} {rating:4.1f}/10")
    
    # 4. Taxa de Sucesso Financeiro
    print("\n\n4. TAXA DE SUCESSO FINANCEIRO (%)")
    print("-" * 50)
    
    cluster_success = defaultdict(lambda: {'total': 0, 'success': 0})
    for row in data:
        cluster = row['cluster']
        profit = convert_to_numeric(row['revenue']) - convert_to_numeric(row['budget'])
        
        cluster_success[cluster]['total'] += 1
        if profit and profit > 0:
            cluster_success[cluster]['success'] += 1
    
    success_rates = {}
    for cluster, stats in cluster_success.items():
        if stats['total'] > 0:
            success_rates[cluster] = (stats['success'] / stats['total']) * 100
    
    max_rate = max(success_rates.values()) if success_rates else 100
    max_bar_length = 25
    
    for cluster, rate in sorted(success_rates.items(), key=lambda x: x[1], reverse=True):
        bar_length = int((rate / max_rate) * max_bar_length)
        bar = "█" * bar_length
        print(f"{cluster:15} | {bar} {rate:5.1f}%")

def create_matplotlib_graphs(data):
    """Cria gráficos usando matplotlib (se disponível)"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        print("\n" + "="*80)
        print("CRIANDO GRÁFICOS COM MATPLOTLIB")
        print("="*80)
        
        # Configurar estilo
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        
        # Criar pasta para salvar gráficos
        os.makedirs('graphs', exist_ok=True)
        
        # 1. Distribuição dos Clusters
        cluster_counts = defaultdict(int)
        for row in data:
            cluster_counts[row['cluster']] += 1
        
        clusters = list(cluster_counts.keys())
        counts = list(cluster_counts.values())
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Gráfico de barras
        colors = plt.cm.Set3(np.linspace(0, 1, len(clusters)))
        bars = ax1.bar(clusters, counts, color=colors)
        ax1.set_title('Distribuição dos Clusters', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Clusters')
        ax1.set_ylabel('Número de Filmes')
        ax1.tick_params(axis='x', rotation=45)
        
        # Adicionar valores nas barras
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                     str(count), ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de pizza
        ax2.pie(counts, labels=clusters, autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('Proporção dos Clusters', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('graphs/01_cluster_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Performance Financeira
        cluster_stats = defaultdict(lambda: {
            'budgets': [], 'revenues': [], 'profits': [], 'rois': []
        })
        
        for row in data:
            cluster = row['cluster']
            budget = convert_to_numeric(row['budget'])
            revenue = convert_to_numeric(row['revenue'])
            
            if budget and revenue and budget > 0:
                profit = revenue - budget
                roi = (profit / budget) * 100
                
                cluster_stats[cluster]['budgets'].append(budget)
                cluster_stats[cluster]['revenues'].append(revenue)
                cluster_stats[cluster]['profits'].append(profit)
                cluster_stats[cluster]['rois'].append(roi)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Orçamento médio
        budget_means = {k: statistics.mean(v['budgets'])/1e6 for k, v in cluster_stats.items() if v['budgets']}
        axes[0,0].bar(budget_means.keys(), budget_means.values(), color='skyblue')
        axes[0,0].set_title('Orçamento Médio por Cluster (Milhões $)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Receita média
        revenue_means = {k: statistics.mean(v['revenues'])/1e6 for k, v in cluster_stats.items() if v['revenues']}
        axes[0,1].bar(revenue_means.keys(), revenue_means.values(), color='lightgreen')
        axes[0,1].set_title('Receita Média por Cluster (Milhões $)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Lucro médio
        profit_means = {k: statistics.mean(v['profits'])/1e6 for k, v in cluster_stats.items() if v['profits']}
        colors = ['red' if x < 0 else 'green' for x in profit_means.values()]
        axes[1,0].bar(profit_means.keys(), profit_means.values(), color=colors)
        axes[1,0].set_title('Lucro Médio por Cluster (Milhões $)')
        axes[1,0].tick_params(axis='x', rotation=45)
        axes[1,0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        # ROI médio
        roi_means = {k: statistics.mean(v['rois']) for k, v in cluster_stats.items() if v['rois']}
        colors = ['red' if x < 0 else 'green' for x in roi_means.values()]
        axes[1,1].bar(roi_means.keys(), roi_means.values(), color=colors)
        axes[1,1].set_title('ROI Médio por Cluster (%)')
        axes[1,1].tick_params(axis='x', rotation=45)
        axes[1,1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig('graphs/02_financial_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 3. Avaliações de Qualidade
        cluster_ratings = defaultdict(lambda: {
            'imdb': [], 'rotten': [], 'metacritic': []
        })
        
        for row in data:
            cluster = row['cluster']
            imdb = convert_to_numeric(row['imdb'])
            rotten = convert_to_numeric(row['rotten'])
            metacritic = convert_to_numeric(row['Metacritic'])
            
            if imdb:
                cluster_ratings[cluster]['imdb'].append(imdb)
            if rotten:
                cluster_ratings[cluster]['rotten'].append(rotten)
            if metacritic:
                cluster_ratings[cluster]['metacritic'].append(metacritic)
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # IMDB
        imdb_means = {k: statistics.mean(v['imdb']) for k, v in cluster_ratings.items() if v['imdb']}
        axes[0].bar(imdb_means.keys(), imdb_means.values(), color='gold')
        axes[0].set_title('Avaliação IMDB Média por Cluster')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].set_ylabel('IMDB Rating')
        
        # Rotten Tomatoes
        rotten_means = {k: statistics.mean(v['rotten']) for k, v in cluster_ratings.items() if v['rotten']}
        axes[1].bar(rotten_means.keys(), rotten_means.values(), color='red')
        axes[1].set_title('Avaliação Rotten Tomatoes Média por Cluster')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].set_ylabel('Rotten Tomatoes (%)')
        
        # Metacritic
        metacritic_means = {k: statistics.mean(v['metacritic']) for k, v in cluster_ratings.items() if v['metacritic']}
        axes[2].bar(metacritic_means.keys(), metacritic_means.values(), color='blue')
        axes[2].set_title('Avaliação Metacritic Média por Cluster')
        axes[2].tick_params(axis='x', rotation=45)
        axes[2].set_ylabel('Metacritic Rating')
        
        plt.tight_layout()
        plt.savefig('graphs/03_quality_ratings.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 4. Taxas de Sucesso
        cluster_success = defaultdict(lambda: {
            'total': 0, 'financial_success': 0, 'critical_success': 0
        })
        
        for row in data:
            cluster = row['cluster']
            profit = convert_to_numeric(row['revenue']) - convert_to_numeric(row['budget'])
            imdb = convert_to_numeric(row['imdb'])
            rotten = convert_to_numeric(row['rotten'])
            
            cluster_success[cluster]['total'] += 1
            
            if profit and profit > 0:
                cluster_success[cluster]['financial_success'] += 1
            
            if imdb and rotten and imdb > 7.0 and rotten > 70:
                cluster_success[cluster]['critical_success'] += 1
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Sucesso financeiro
        financial_rates = {k: (v['financial_success'] / v['total']) * 100 
                          for k, v in cluster_success.items()}
        axes[0].bar(financial_rates.keys(), financial_rates.values(), color='green')
        axes[0].set_title('Taxa de Sucesso Financeiro por Cluster')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].set_ylabel('Taxa de Sucesso (%)')
        
        # Sucesso crítico
        critical_rates = {k: (v['critical_success'] / v['total']) * 100 
                         for k, v in cluster_success.items()}
        axes[1].bar(critical_rates.keys(), critical_rates.values(), color='purple')
        axes[1].set_title('Taxa de Sucesso Crítico por Cluster')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].set_ylabel('Taxa de Sucesso (%)')
        
        plt.tight_layout()
        plt.savefig('graphs/04_success_rates.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 5. Scatter Plot: Orçamento vs Receita
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        axes = axes.ravel()
        
        for i, cluster in enumerate(cluster_stats.keys()):
            if cluster in cluster_stats and cluster_stats[cluster]['budgets']:
                budgets = [b/1e6 for b in cluster_stats[cluster]['budgets']]
                revenues = [r/1e6 for r in cluster_stats[cluster]['revenues']]
                
                axes[i].scatter(budgets, revenues, alpha=0.6, s=20)
                axes[i].set_xlabel('Orçamento (Milhões $)')
                axes[i].set_ylabel('Receita (Milhões $)')
                axes[i].set_title(f'{cluster}')
                axes[i].grid(True, alpha=0.3)
                
                # Linha de break-even
                max_budget = max(budgets) if budgets else 100
                axes[i].plot([0, max_budget], [0, max_budget], 'r--', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig('graphs/05_budget_vs_revenue.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("\nGráficos salvos na pasta 'graphs/'")
        
    except ImportError:
        print("Matplotlib não está disponível. Use a função create_text_charts() para visualizações em texto.")

def main():
    """Função principal"""
    print("CRIAÇÃO DE GRÁFICOS PARA ANÁLISE DOS CLUSTERS")
    print("=" * 60)
    
    # Carregar dados
    data = load_data()
    
    # Criar gráficos em texto
    create_text_charts(data)
    
    # Tentar criar gráficos com matplotlib
    create_matplotlib_graphs(data)
    
    print("\nAnálise de gráficos concluída!")

if __name__ == "__main__":
    main() 