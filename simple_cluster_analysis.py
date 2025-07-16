"""
Análise Simples dos Clusters de Filmes
======================================

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

import csv
from collections import defaultdict
import statistics

def load_data():
    """Carrega o dataset CSV"""
    print("Carregando dataset_com_cluster.csv...")
    
    data = []
    with open('dataset_com_cluster.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Pular linha de cabeçalho duplicada
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

def analyze_cluster_distribution(data):
    """Analisa a distribuição dos clusters"""
    print("\n=== DISTRIBUIÇÃO DOS CLUSTERS ===")
    
    cluster_counts = defaultdict(int)
    for row in data:
        cluster_counts[row['cluster']] += 1
    
    total_films = len(data)
    print(f"Total de filmes: {total_films}")
    print("\nDistribuição por cluster:")
    
    for cluster, count in sorted(cluster_counts.items()):
        percentage = (count / total_films) * 100
        print(f"  {cluster}: {count} filmes ({percentage:.1f}%)")
    
    return cluster_counts

def analyze_financial_performance(data):
    """Analisa performance financeira por cluster"""
    print("\n=== PERFORMANCE FINANCEIRA POR CLUSTER ===")
    
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
    
    print("\nEstatísticas financeiras por cluster:")
    print("-" * 80)
    
    for cluster, stats in cluster_stats.items():
        if stats['budgets']:
            avg_budget = statistics.mean(stats['budgets']) / 1e6
            avg_revenue = statistics.mean(stats['revenues']) / 1e6
            avg_profit = statistics.mean(stats['profits']) / 1e6
            avg_roi = statistics.mean(stats['rois'])
            
            print(f"\n{cluster}:")
            print(f"  Orçamento médio: ${avg_budget:.1f}M")
            print(f"  Receita média: ${avg_revenue:.1f}M")
            print(f"  Lucro médio: ${avg_profit:.1f}M")
            print(f"  ROI médio: {avg_roi:.1f}%")
            print(f"  Número de filmes: {len(stats['budgets'])}")

def analyze_quality_ratings(data):
    """Analisa avaliações de qualidade por cluster"""
    print("\n=== AVALIAÇÕES DE QUALIDADE POR CLUSTER ===")
    
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
    
    print("\nAvaliações médias por cluster:")
    print("-" * 50)
    
    for cluster, ratings in cluster_ratings.items():
        print(f"\n{cluster}:")
        if ratings['imdb']:
            avg_imdb = statistics.mean(ratings['imdb'])
            print(f"  IMDB: {avg_imdb:.1f}/10")
        if ratings['rotten']:
            avg_rotten = statistics.mean(ratings['rotten'])
            print(f"  Rotten Tomatoes: {avg_rotten:.1f}%")
        if ratings['metacritic']:
            avg_metacritic = statistics.mean(ratings['metacritic'])
            print(f"  Metacritic: {avg_metacritic:.1f}/100")

def analyze_success_rates(data):
    """Analisa taxas de sucesso por cluster"""
    print("\n=== TAXAS DE SUCESSO POR CLUSTER ===")
    
    cluster_success = defaultdict(lambda: {
        'total': 0, 'financial_success': 0, 'critical_success': 0
    })
    
    for row in data:
        cluster = row['cluster']
        profit = convert_to_numeric(row['revenue']) - convert_to_numeric(row['budget'])
        imdb = convert_to_numeric(row['imdb'])
        rotten = convert_to_numeric(row['rotten'])
        
        cluster_success[cluster]['total'] += 1
        
        # Sucesso financeiro (lucro positivo)
        if profit and profit > 0:
            cluster_success[cluster]['financial_success'] += 1
        
        # Sucesso crítico (boas avaliações)
        if imdb and rotten and imdb > 7.0 and rotten > 70:
            cluster_success[cluster]['critical_success'] += 1
    
    print("\nTaxas de sucesso por cluster:")
    print("-" * 50)
    
    for cluster, success in cluster_success.items():
        financial_rate = (success['financial_success'] / success['total']) * 100
        critical_rate = (success['critical_success'] / success['total']) * 100
        
        print(f"\n{cluster}:")
        print(f"  Sucesso financeiro: {financial_rate:.1f}%")
        print(f"  Sucesso crítico: {critical_rate:.1f}%")
        print(f"  Total de filmes: {success['total']}")

def analyze_top_performers(data):
    """Identifica os melhores filmes por cluster"""
    print("\n=== TOP PERFORMERS POR CLUSTER ===")
    
    cluster_best = defaultdict(list)
    
    for row in data:
        cluster = row['cluster']
        title = row['Title']
        profit = convert_to_numeric(row['revenue']) - convert_to_numeric(row['budget'])
        imdb = convert_to_numeric(row['imdb'])
        year = row['Year']
        
        if profit:
            cluster_best[cluster].append({
                'title': title,
                'year': year,
                'profit': profit,
                'imdb': imdb
            })
    
    print("\nTop 5 filmes mais lucrativos por cluster:")
    print("-" * 60)
    
    for cluster, films in cluster_best.items():
        # Ordenar por lucro
        films.sort(key=lambda x: x['profit'], reverse=True)
        top_5 = films[:5]
        
        print(f"\n{cluster}:")
        for i, film in enumerate(top_5, 1):
            profit_millions = film['profit'] / 1e6
            imdb_rating = f"{film['imdb']:.1f}" if film['imdb'] else "N/A"
            print(f"  {i}. {film['title']} ({film['year']}) - ${profit_millions:.1f}M (IMDB: {imdb_rating})")

def generate_insights(data):
    """Gera insights principais"""
    print("\n" + "=" * 80)
    print("INSIGHTS PRINCIPAIS")
    print("=" * 80)
    
    # Análise financeira
    cluster_profits = defaultdict(list)
    for row in data:
        cluster = row['cluster']
        profit = convert_to_numeric(row['revenue']) - convert_to_numeric(row['budget'])
        if profit:
            cluster_profits[cluster].append(profit)
    
    # Clusters mais lucrativos
    avg_profits = {}
    for cluster, profits in cluster_profits.items():
        avg_profits[cluster] = statistics.mean(profits)
    
    most_profitable = max(avg_profits.items(), key=lambda x: x[1])
    least_profitable = min(avg_profits.items(), key=lambda x: x[1])
    
    print(f"\n1. CLUSTER MAIS LUCRATIVO: {most_profitable[0]}")
    print(f"   Lucro médio: ${most_profitable[1]/1e6:.1f}M")
    
    print(f"\n2. CLUSTER MENOS LUCRATIVO: {least_profitable[0]}")
    print(f"   Lucro médio: ${least_profitable[1]/1e6:.1f}M")
    
    # Análise de qualidade
    cluster_imdb = defaultdict(list)
    for row in data:
        cluster = row['cluster']
        imdb = convert_to_numeric(row['imdb'])
        if imdb:
            cluster_imdb[cluster].append(imdb)
    
    best_rated = max(cluster_imdb.items(), key=lambda x: statistics.mean(x[1]))
    print(f"\n3. CLUSTER COM MELHORES AVALIAÇÕES: {best_rated[0]}")
    print(f"   Avaliação IMDB média: {statistics.mean(best_rated[1]):.1f}/10")
    
    # Análise de volume
    cluster_counts = defaultdict(int)
    for row in data:
        cluster_counts[row['cluster']] += 1
    
    largest_cluster = max(cluster_counts.items(), key=lambda x: x[1])
    smallest_cluster = min(cluster_counts.items(), key=lambda x: x[1])
    
    print(f"\n4. CLUSTER MAIS REPRESENTADO: {largest_cluster[0]}")
    print(f"   Número de filmes: {largest_cluster[1]}")
    
    print(f"\n5. CLUSTER MENOS REPRESENTADO: {smallest_cluster[0]}")
    print(f"   Número de filmes: {smallest_cluster[1]}")
    
    print("\n" + "=" * 80)

def main():
    """Função principal"""
    print("ANÁLISE DOS CLUSTERS DE FILMES")
    print("=" * 50)
    
    # Carregar dados
    data = load_data()
    
    # Executar análises
    analyze_cluster_distribution(data)
    analyze_financial_performance(data)
    analyze_quality_ratings(data)
    analyze_success_rates(data)
    analyze_top_performers(data)
    generate_insights(data)
    
    print("\nAnálise concluída!")

if __name__ == "__main__":
    main() 