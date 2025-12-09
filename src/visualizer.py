import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
import os


class Visualizer:
    
    def __init__(self, output_dir: str = 'output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_open_time_histogram(self, open_times: List[int]):
        plt.figure(figsize=(12, 6))
        plt.hist(open_times, bins=50, edgecolor='black', color='hotpink')
        plt.xlabel('Время в открытом состоянии (дни)')
        plt.ylabel('Количество задач')
        plt.title('Распределение задач по времени в открытом состоянии')
        plt.grid(True, alpha=0.3)
        plt.savefig(f'{self.output_dir}/1_open_time_histogram.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_status_durations(self, status_durations: Dict[str, List[int]]):
        if not status_durations:
            print("⚠️  Нет данных о статусах")
            plt.figure(figsize=(12, 6))
            plt.text(0.5, 0.5, 'Нет данных о длительности статусов\n(требуется changelog)', 
                     ha='center', va='center', fontsize=14)
            plt.axis('off')
            plt.savefig(f'{self.output_dir}/2_status_durations.png', dpi=300, bbox_inches='tight')
            plt.close()
            return
        
        num_statuses = len(status_durations)
        fig, axes = plt.subplots(num_statuses, 1, figsize=(12, 4 * num_statuses))
        if num_statuses == 1:
            axes = [axes]
        
        for ax, (status, durations) in zip(axes, status_durations.items()):
            if durations:
                ax.hist(durations, bins=30, edgecolor='black', color='hotpink')
                ax.set_xlabel('Время в статусе (дни)')
                ax.set_ylabel('Количество задач')
                ax.set_title(f'Распределение времени в статусе: {status}')
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/2_status_durations.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_daily_stats(self, df: pd.DataFrame):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        ax1.plot(df['date'], df['created'], label='Созданные', marker='o', markersize=2, color='hotpink')
        ax1.plot(df['date'], df['closed'], label='Закрытые', marker='o', markersize=2, color='skyblue')
        ax1.set_xlabel('Дата')
        ax1.set_ylabel('Количество задач')
        ax1.set_title('Созданные и закрытые задачи по дням')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(df['date'], df['created_cumsum'], label='Накопительно созданные', linewidth=2, color='hotpink')
        ax2.plot(df['date'], df['closed_cumsum'], label='Накопительно закрытые', linewidth=2, color='skyblue')
        ax2.set_xlabel('Дата')
        ax2.set_ylabel('Накопительное количество')
        ax2.set_title('Накопительные итоги')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/3_daily_stats.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_user_stats(self, df: pd.DataFrame):
        plt.figure(figsize=(12, 10))
        plt.barh(df['user'], df['count'], color='hotpink', edgecolor='black')
        plt.xlabel('Количество задач')
        plt.ylabel('Пользователь')
        plt.title('Топ-30 пользователей по количеству задач')
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/4_user_stats.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_time_in_progress_histogram(self, time_in_progress: List[float]):
        if not time_in_progress:
            print("⚠️  Нет данных о времени в In Progress")
            plt.figure(figsize=(12, 6))
            plt.text(0.5, 0.5, 'Нет данных о времени в статусе In Progress\n(требуется changelog)', 
                     ha='center', va='center', fontsize=14)
            plt.axis('off')
            plt.savefig(f'{self.output_dir}/5_time_in_progress_histogram.png', dpi=300, bbox_inches='tight')
            plt.close()
            return
        
        print(f"📊 График In Progress: {len(time_in_progress)} задач")
        
        plt.figure(figsize=(12, 6))
        num_bins = min(50, max(10, len(time_in_progress) // 10))
        plt.hist(time_in_progress, bins=num_bins, edgecolor='black', alpha=0.7, color='hotpink')
        
        plt.xlabel('Время в статусе In Progress (часы)')
        plt.ylabel('Количество задач')
        plt.title(f'Распределение задач по времени в статусе In Progress\n(всего {len(time_in_progress)} задач)')
        plt.grid(True, alpha=0.3)
        
        avg_time = sum(time_in_progress) / len(time_in_progress)
        median_time = sorted(time_in_progress)[len(time_in_progress) // 2]
        
        plt.axvline(avg_time, color='red', linestyle='--', linewidth=2, 
                   label=f'Среднее: {avg_time:.1f}ч ({avg_time/24:.1f} дней)')
        plt.axvline(median_time, color='green', linestyle='--', linewidth=2, 
                   label=f'Медиана: {median_time:.1f}ч ({median_time/24:.1f} дней)')
        plt.legend()
        
        stats_text = f'Min: {min(time_in_progress):.1f}ч\nMax: {max(time_in_progress):.1f}ч'
        plt.text(0.98, 0.98, stats_text, transform=plt.gca().transAxes, 
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(boxstyle='round', facecolor='pink', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/5_time_in_progress_histogram.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✓ Среднее: {avg_time:.1f}ч ({avg_time/24:.1f} дней)")
        print(f"   ✓ Медиана: {median_time:.1f}ч ({median_time/24:.1f} дней)")
    
    def plot_priority_distribution(self, priority_counts: Dict[str, int]):
        plt.figure(figsize=(10, 6))
        priorities = list(priority_counts.keys())
        counts = list(priority_counts.values())
        
        plt.bar(priorities, counts, edgecolor='black', color='hotpink')
        plt.xlabel('Приоритет')
        plt.ylabel('Количество задач')
        plt.title('Распределение задач по приоритету')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/6_priority_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
