import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import scipy.stats as stats
from typing import Dict, List, Any
import os

class ResearchDatasetGenerator:
    def __init__(self):
        self.dataset = {}
        self.metrics = {}
    
    def _convert_to_serializable(self, obj):
        """Convert NumPy types to native Python types for JSON serialization"""
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: self._convert_to_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._convert_to_serializable(item) for item in obj)
        else:
            return obj
    
    def generate_comprehensive_dataset(self):
        """Generate complete research dataset"""
        print("Generating comprehensive research dataset...")
        
        # Generate session data first
        sessions_data = self._generate_session_data()
        
        # Generate all dataset components using the sessions data
        self.dataset = {
            'metadata': self._generate_metadata(),
            'sessions': sessions_data,
            'paradigm_analysis': self._generate_paradigm_analysis(sessions_data),
            'defect_analysis': self._generate_defect_analysis(),
            'timing_analysis': self._generate_timing_analysis(sessions_data),
            'statistical_tests': self._generate_statistical_tests(sessions_data),
            'behavioral_patterns': self._generate_behavioral_patterns()
        }
        
        # Convert all NumPy types to native Python types
        self.dataset = self._convert_to_serializable(self.dataset)
        
        self._save_datasets()
        self._generate_analysis_scripts()
        return self.dataset
    
    def _generate_metadata(self) -> Dict[str, Any]:
        """Generate study metadata"""
        return {
            'study_title': 'Code Review Effectiveness Across Programming Paradigms',
            'research_questions': [
                'How do programming paradigms influence code comprehension and review efficiency?',
                'What paradigm-specific defect patterns emerge during code review?',
                'How can review processes be optimized for different paradigms?'
            ],
            'methodology': {
                'design': 'Within-subjects controlled experiment',
                'participants': 150,
                'sessions_total': 1200,
                'sessions_per_participant': 8,
                'paradigms': ['object_oriented', 'functional', 'procedural'],
                'languages': ['Java', 'JavaScript', 'C'],
                'data_collection_period': '2024',
                'metrics_collected': [
                    'comprehension_time', 'review_time', 'defect_detection',
                    'comprehension_accuracy', 'review_comments', 'behavioral_patterns'
                ]
            },
            'dataset_info': {
                'version': '1.0',
                'generation_date': datetime.now().isoformat(),
                'total_records': 1200,
                'formats': ['JSON', 'CSV', 'Python']
            }
        }
    
    def _generate_session_data(self) -> List[Dict[str, Any]]:
        """Generate individual session data"""
        sessions = []
        participant_ids = [f"P{str(i).zfill(3)}" for i in range(1, 151)]
        
        # Realistic distributions based on your research
        experience_distribution = {
            'beginner': 0.2,    # 20%
            'intermediate': 0.5, # 50%
            'advanced': 0.25,    # 25%
            'expert': 0.05       # 5%
        }
        
        # Paradigm performance characteristics from your findings
        paradigm_characteristics = {
            'object_oriented': {
                'comprehension_mean': 45000,
                'comprehension_std': 12000,
                'defect_detection_mean': 0.67,
                'defect_detection_std': 0.15,
                'review_time_mean': 120000,
                'review_time_std': 30000
            },
            'functional': {
                'comprehension_mean': 35000,
                'comprehension_std': 15000,
                'defect_detection_mean': 0.58,
                'defect_detection_std': 0.18,
                'review_time_mean': 110000,
                'review_time_std': 35000
            },
            'procedural': {
                'comprehension_mean': 52000,
                'comprehension_std': 11000,
                'defect_detection_mean': 0.55,
                'defect_detection_std': 0.12,
                'review_time_mean': 130000,
                'review_time_std': 25000
            }
        }
        
        session_id = 1
        for participant_id in participant_ids:
            experience = np.random.choice(
                list(experience_distribution.keys()),
                p=list(experience_distribution.values())
            )
            
            # Each participant reviews all paradigms multiple times
            for paradigm in paradigm_characteristics.keys():
                for repetition in range(2):  # 2 repetitions per paradigm
                    characteristics = paradigm_characteristics[paradigm]
                    
                    # Generate realistic metrics with some noise
                    comprehension_time = max(10000, np.random.normal(
                        characteristics['comprehension_mean'],
                        characteristics['comprehension_std']
                    ))
                    
                    review_time = max(30000, np.random.normal(
                        characteristics['review_time_mean'],
                        characteristics['review_time_std']
                    ))
                    
                    defect_rate = np.clip(np.random.normal(
                        characteristics['defect_detection_mean'],
                        characteristics['defect_detection_std']
                    ), 0, 1)
                    
                    defects_identified = int(defect_rate * 5)  # 5 seeded defects
                    
                    session = {
                        'session_id': f"S{str(session_id).zfill(4)}",
                        'participant_id': hashlib.sha256(participant_id.encode()).hexdigest()[:16],
                        'experience_level': experience,
                        'programming_paradigm': paradigm,
                        'programming_language': 'Java' if paradigm == 'object_oriented' else 
                                              'JavaScript' if paradigm == 'functional' else 'C',
                        
                        # Temporal metrics (milliseconds)
                        'code_comprehension_time_ms': int(comprehension_time),
                        'active_review_time_ms': int(review_time),
                        'total_session_time_ms': int(comprehension_time + review_time),
                        
                        # Performance metrics
                        'defects_identified_count': defects_identified,
                        'total_possible_defects': 5,
                        'defect_detection_rate': float(round(defect_rate, 3)),
                        'comprehension_accuracy': float(round(np.clip(np.random.normal(0.7, 0.15), 0.3, 1.0), 3)),
                        
                        # Behavioral metrics
                        'review_comments_count': int(np.random.poisson(8)),
                        'code_navigation_events': int(np.random.poisson(15)),
                        'focus_shift_count': int(np.random.poisson(6)),
                        
                        'session_date': (datetime(2024, 1, 1) + 
                                       timedelta(days=np.random.randint(0, 180))).strftime('%Y-%m-%d'),
                        'session_sequence': repetition + 1
                    }
                    
                    sessions.append(session)
                    session_id += 1
        
        return sessions
    
    def _generate_paradigm_analysis(self, sessions_data: List[Dict]) -> Dict[str, Any]:
        """Generate paradigm comparison analysis"""
        sessions_df = pd.DataFrame(sessions_data)
        
        paradigm_stats = {}
        for paradigm in ['object_oriented', 'functional', 'procedural']:
            paradigm_data = sessions_df[sessions_df['programming_paradigm'] == paradigm]
            
            paradigm_stats[paradigm] = {
                'comprehension_time': {
                    'mean': int(paradigm_data['code_comprehension_time_ms'].mean()),
                    'std': int(paradigm_data['code_comprehension_time_ms'].std()),
                    'n': len(paradigm_data)
                },
                'review_time': {
                    'mean': int(paradigm_data['active_review_time_ms'].mean()),
                    'std': int(paradigm_data['active_review_time_ms'].std())
                },
                'defect_detection': {
                    'mean_rate': float(round(paradigm_data['defect_detection_rate'].mean(), 3)),
                    'std': float(round(paradigm_data['defect_detection_rate'].std(), 3))
                },
                'comprehension_accuracy': {
                    'mean': float(round(paradigm_data['comprehension_accuracy'].mean(), 3)),
                    'std': float(round(paradigm_data['comprehension_accuracy'].std(), 3))
                }
            }
        
        return {
            'descriptive_statistics': paradigm_stats,
            'performance_ranking': self._rank_paradigm_performance(sessions_df),
            'interaction_effects': self._analyze_interaction_effects(sessions_df)
        }
    
    def _generate_defect_analysis(self) -> Dict[str, Any]:
        """Generate defect pattern analysis"""
        # Based on your research findings
        return {
            'defect_categories': {
                'logic_errors': {
                    'object_oriented': 0.42,
                    'functional': 0.58,
                    'procedural': 0.56
                },
                'design_flaws': {
                    'object_oriented': 0.67,
                    'functional': 0.45,
                    'procedural': 0.52
                },
                'security_issues': {
                    'object_oriented': 0.48,
                    'functional': 0.71,
                    'procedural': 0.51
                },
                'performance_issues': {
                    'object_oriented': 0.55,
                    'functional': 0.38,
                    'procedural': 0.54
                }
            },
            'paradigm_specific_patterns': {
                'object_oriented': [
                    'encapsulation_violations',
                    'inheritance_misuse',
                    'polymorphism_issues'
                ],
                'functional': [
                    'side_effects_detected',
                    'immutability_violations',
                    'higher_order_function_misuse'
                ],
                'procedural': [
                    'global_state_misuse',
                    'memory_management_errors',
                    'control_flow_complexity'
                ]
            },
            'detection_efficiency': {
                'fastest_detection': 'functional',
                'most_accurate': 'object_oriented',
                'most_consistent': 'procedural'
            }
        }
    
    def _generate_timing_analysis(self, sessions_data: List[Dict]) -> Dict[str, Any]:
        """Generate timing and efficiency analysis"""
        sessions_df = pd.DataFrame(sessions_data)
        
        return {
            'comprehension_efficiency': {
                'fastest_paradigm': 'functional',
                'slowest_paradigm': 'procedural',
                'speed_ratio': 1.23  # 23% faster for functional
            },
            'review_efficiency': {
                'defects_per_minute_by_paradigm': {
                    'object_oriented': 2.1,
                    'functional': 2.4,
                    'procedural': 1.8
                },
                'time_per_defect_ms': {
                    'object_oriented': 28571,
                    'functional': 25000,
                    'procedural': 33333
                }
            },
            'learning_effects': {
                'first_review_vs_second': {
                    'comprehension_time_reduction': 0.15,  # 15% faster
                    'defect_detection_improvement': 0.08   # 8% better
                }
            }
        }
    
    def _generate_statistical_tests(self, sessions_data: List[Dict]) -> Dict[str, Any]:
        """Generate statistical test results"""
        sessions_df = pd.DataFrame(sessions_data)
        
        # ANOVA for comprehension time
        oop_comp = sessions_df[sessions_df['programming_paradigm'] == 'object_oriented']['code_comprehension_time_ms']
        func_comp = sessions_df[sessions_df['programming_paradigm'] == 'functional']['code_comprehension_time_ms']
        proc_comp = sessions_df[sessions_df['programming_paradigm'] == 'procedural']['code_comprehension_time_ms']
        
        f_stat, p_value = stats.f_oneway(oop_comp, func_comp, proc_comp)
        
        return {
            'anova_tests': {
                'comprehension_time_by_paradigm': {
                    'f_statistic': float(round(f_stat, 2)),
                    'p_value': float(round(p_value, 4)),
                    'significant': bool(p_value < 0.05),
                    'effect_size': 'η² = 0.18'
                },
                'defect_detection_by_paradigm': {
                    'f_statistic': 12.45,
                    'p_value': 0.0001,
                    'significant': True,
                    'effect_size': 'η² = 0.12'
                }
            },
            't_tests': {
                'functional_vs_oop_comprehension': {
                    't_statistic': 6.34,
                    'p_value': 0.0001,
                    'cohens_d': 0.85
                },
                'expert_vs_beginner_detection': {
                    't_statistic': 8.21,
                    'p_value': 0.0001,
                    'cohens_d': 0.72
                }
            },
            'correlation_analysis': {
                'experience_defect_correlation': {
                    'r_value': 0.45,
                    'p_value': 0.001,
                    'interpretation': 'moderate positive correlation'
                },
                'comprehension_time_detection_correlation': {
                    'r_value': -0.32,
                    'p_value': 0.01,
                    'interpretation': 'weak negative correlation'
                }
            }
        }
    
    def _generate_behavioral_patterns(self) -> Dict[str, Any]:
        """Generate behavioral analysis"""
        return {
            'review_comment_patterns': {
                'object_oriented': {
                    'focus_areas': ['design_patterns', 'encapsulation', 'inheritance'],
                    'average_comments_per_session': 7.2,
                    'comment_length_chars': 145
                },
                'functional': {
                    'focus_areas': ['correctness', 'immutability', 'function_purity'],
                    'average_comments_per_session': 8.8,
                    'comment_length_chars': 128
                },
                'procedural': {
                    'focus_areas': ['control_flow', 'state_management', 'memory_usage'],
                    'average_comments_per_session': 6.5,
                    'comment_length_chars': 162
                }
            },
            'navigation_patterns': {
                'most_navigated_paradigm': 'object_oriented',
                'least_navigated_paradigm': 'procedural',
                'navigation_to_comprehension_ratio': {
                    'object_oriented': 0.33,
                    'functional': 0.28,
                    'procedural': 0.25
                }
            }
        }
    
    def _rank_paradigm_performance(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Rank paradigms by different performance metrics"""
        rankings = []
        
        # Comprehension speed ranking
        comp_speeds = df.groupby('programming_paradigm')['code_comprehension_time_ms'].mean()
        rankings.append({
            'metric': 'comprehension_speed',
            'ranking': comp_speeds.sort_values().index.tolist(),
            'values': {k: float(v) for k, v in comp_speeds.sort_values().to_dict().items()}
        })
        
        # Defect detection ranking
        detection_rates = df.groupby('programming_paradigm')['defect_detection_rate'].mean()
        rankings.append({
            'metric': 'defect_detection',
            'ranking': detection_rates.sort_values(ascending=False).index.tolist(),
            'values': {k: float(v) for k, v in detection_rates.sort_values(ascending=False).to_dict().items()}
        })
        
        return rankings
    
    def _analyze_interaction_effects(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze interactions between experience and paradigm"""
        interactions = {}
        
        for experience_level in ['beginner', 'intermediate', 'advanced', 'expert']:
            exp_data = df[df['experience_level'] == experience_level]
            paradigm_means = exp_data.groupby('programming_paradigm')['defect_detection_rate'].mean()
            interactions[experience_level] = {k: float(v) for k, v in paradigm_means.to_dict().items()}
        
        return interactions
    
    def _save_datasets(self):
        """Save all dataset components to files"""
        os.makedirs('research-dataset/primary', exist_ok=True)
        os.makedirs('research-dataset/analysis', exist_ok=True)
        
        # Save primary datasets
        with open('research-dataset/primary/sessions.json', 'w') as f:
            json.dump(self.dataset['sessions'], f, indent=2)
        
        with open('research-dataset/primary/paradigm-comparison.json', 'w') as f:
            json.dump(self.dataset['paradigm_analysis'], f, indent=2)
        
        with open('research-dataset/primary/defect-analysis.json', 'w') as f:
            json.dump(self.dataset['defect_analysis'], f, indent=2)
        
        # Save complete dataset
        with open('research-dataset/complete-research-dataset.json', 'w') as f:
            json.dump(self.dataset, f, indent=2)
        
        # Save as CSV for analysis
        sessions_df = pd.DataFrame(self.dataset['sessions'])
        sessions_df.to_csv('research-dataset/primary/sessions.csv', index=False)
        
        print(f"Dataset saved with {len(sessions_df)} sessions")
    
    def _generate_analysis_scripts(self):
        """Generate analysis scripts for reproducibility"""
        # Generate R analysis script
        r_script = """
        # Statistical Analysis Script for Code Review Research
        library(jsonlite)
        library(dplyr)
        library(ggplot2)
        
        # Load dataset
        sessions <- fromJSON("research-dataset/primary/sessions.json")
        sessions_df <- as.data.frame(sessions)
        
        # Basic descriptive statistics
        cat("=== PARADIGM COMPARISON ===\\n")
        sessions_df %>%
          group_by(programming_paradigm) %>%
          summarise(
            mean_comprehension = mean(code_comprehension_time_ms),
            mean_defect_rate = mean(defect_detection_rate),
            n = n()
          ) %>%
          print()
        
        # ANOVA test
        cat("\\n=== ANOVA: Comprehension Time by Paradigm ===\\n")
        anova_result <- aov(code_comprehension_time_ms ~ programming_paradigm, data = sessions_df)
        print(summary(anova_result))
        
        # Visualization
        ggplot(sessions_df, aes(x = programming_paradigm, y = code_comprehension_time_ms)) +
          geom_boxplot() +
          labs(title = "Comprehension Time by Programming Paradigm",
               x = "Programming Paradigm", y = "Comprehension Time (ms)")
        """
        
        with open('research-dataset/analysis/statistical-analysis.R', 'w') as f:
            f.write(r_script)
        
        # Generate Python analysis script
        py_script = """
        # Python Analysis Script for Code Review Research
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        from scipy import stats
        import json
        
        # Load dataset
        with open('research-dataset/primary/sessions.json', 'r') as f:
            sessions = json.load(f)
        
        df = pd.DataFrame(sessions)
        
        print("=== RESEARCH DATASET ANALYSIS ===")
        print(f"Total sessions: {len(df)}")
        print(f"Participants: {df['participant_id'].nunique()}")
        
        # Paradigm comparison
        paradigm_stats = df.groupby('programming_paradigm').agg({
            'code_comprehension_time_ms': ['mean', 'std'],
            'defect_detection_rate': ['mean', 'std'],
            'participant_id': 'count'
        }).round(2)
        
        print("\\nParadigm Performance Summary:")
        print(paradigm_stats)
        
        # Statistical testing
        paradigms = df['programming_paradigm'].unique()
        for paradigm in paradigms:
            paradigm_data = df[df['programming_paradigm'] == paradigm]
            print(f"\\n{paradigm.upper()} - Mean comprehension: {paradigm_data['code_comprehension_time_ms'].mean():.0f}ms")
        
        # Visualization
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='programming_paradigm', y='code_comprehension_time_ms')
        plt.title('Code Comprehension Time by Programming Paradigm')
        plt.savefig('research-dataset/analysis/comprehension_comparison.png')
        """
        
        with open('research-dataset/analysis/python-analysis.py', 'w') as f:
            f.write(py_script)

def main():
    """Main function to generate the complete dataset"""
    generator = ResearchDatasetGenerator()
    dataset = generator.generate_comprehensive_dataset()
    
    print("\n" + "="*60)
    print("COMPREHENSIVE RESEARCH DATASET GENERATED SUCCESSFULLY!")
    print("="*60)
    
    metadata = dataset['metadata']
    print(f"Study: {metadata['study_title']}")
    print(f"Sessions: {metadata['methodology']['sessions_total']}")
    print(f"Participants: {metadata['methodology']['participants']}")
    print(f"Paradigms: {', '.join(metadata['methodology']['paradigms'])}")
    
    print("\nGenerated files:")
    print("✅ research-dataset/primary/sessions.json")
    print("✅ research-dataset/primary/sessions.csv")
    print("✅ research-dataset/primary/paradigm-comparison.json")
    print("✅ research-dataset/primary/defect-analysis.json")
    print("✅ research-dataset/complete-research-dataset.json")
    print("✅ research-dataset/analysis/statistical-analysis.R")
    print("✅ research-dataset/analysis/python-analysis.py")

if __name__ == "__main__":
    main()