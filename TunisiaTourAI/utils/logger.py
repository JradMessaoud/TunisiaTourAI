"""
Système de logs pour TunisiaTourAI
Monitoring et débogage de l'application
"""

import logging
import os
from datetime import datetime
from typing import Optional
import json

class TunisiaTourLogger:
    def __init__(self, log_dir: str = "logs", app_name: str = "TunisiaTourAI"):
        """
        Initialise le système de logs
        
        Args:
            log_dir: Répertoire de stockage des logs
            app_name: Nom de l'application
        """
        self.log_dir = log_dir
        self.app_name = app_name
        
        # Créer le répertoire de logs s'il n'existe pas
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configuration du logger principal
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.INFO)
        
        # Éviter les logs dupliqués
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configure les handlers de logs"""
        # Handler pour fichier
        log_file = os.path.join(self.log_dir, f"{self.app_name}_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Handler pour console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Format des logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, extra_data: Optional[dict] = None):
        """
        Log d'information
        
        Args:
            message: Message à logger
            extra_data: Données supplémentaires
        """
        if extra_data:
            message = f"{message} | {json.dumps(extra_data, ensure_ascii=False)}"
        self.logger.info(message)
    
    def warning(self, message: str, extra_data: Optional[dict] = None):
        """
        Log d'avertissement
        
        Args:
            message: Message à logger
            extra_data: Données supplémentaires
        """
        if extra_data:
            message = f"{message} | {json.dumps(extra_data, ensure_ascii=False)}"
        self.logger.warning(message)
    
    def error(self, message: str, extra_data: Optional[dict] = None):
        """
        Log d'erreur
        
        Args:
            message: Message à logger
            extra_data: Données supplémentaires
        """
        if extra_data:
            message = f"{message} | {json.dumps(extra_data, ensure_ascii=False)}"
        self.logger.error(message)
    
    def debug(self, message: str, extra_data: Optional[dict] = None):
        """
        Log de débogage
        
        Args:
            message: Message à logger
            extra_data: Données supplémentaires
        """
        if extra_data:
            message = f"{message} | {json.dumps(extra_data, ensure_ascii=False)}"
        self.logger.debug(message)
    
    def log_ai_request(self, question: str, response: str, duration: float, success: bool):
        """
        Log spécifique pour les requêtes IA
        
        Args:
            question: Question posée
            response: Réponse reçue
            duration: Durée de la requête
            success: Succès de la requête
        """
        extra_data = {
            "type": "ai_request",
            "question_length": len(question),
            "response_length": len(response),
            "duration_seconds": round(duration, 2),
            "success": success
        }
        
        level = self.info if success else self.error
        level(f"IA Request: {question[:100]}...", extra_data)
    
    def log_user_action(self, action: str, user_data: Optional[dict] = None):
        """
        Log des actions utilisateur
        
        Args:
            action: Action effectuée
            user_data: Données utilisateur
        """
        extra_data = {
            "type": "user_action",
            "action": action
        }
        if user_data:
            extra_data.update(user_data)
        
        self.info(f"User Action: {action}", extra_data)
    
    def log_performance(self, operation: str, duration: float, success: bool):
        """
        Log de performance
        
        Args:
            operation: Opération mesurée
            duration: Durée en secondes
            success: Succès de l'opération
        """
        extra_data = {
            "type": "performance",
            "operation": operation,
            "duration_seconds": round(duration, 2),
            "success": success
        }
        
        level = self.info if success else self.warning
        level(f"Performance: {operation}", extra_data)
    
    def get_log_stats(self) -> dict:
        """
        Obtient les statistiques des logs
        
        Returns:
            Dictionnaire avec les statistiques
        """
        try:
            log_files = [f for f in os.listdir(self.log_dir) if f.endswith('.log')]
            total_size = sum(os.path.getsize(os.path.join(self.log_dir, f)) for f in log_files)
            
            return {
                "total_files": len(log_files),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "log_dir": self.log_dir,
                "latest_file": max(log_files) if log_files else None
            }
        except Exception as e:
            return {"error": str(e)}
    
    def cleanup_old_logs(self, days_to_keep: int = 30) -> int:
        """
        Nettoie les anciens logs
        
        Args:
            days_to_keep: Nombre de jours à conserver
            
        Returns:
            Nombre de fichiers supprimés
        """
        import time
        current_time = time.time()
        cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
        
        deleted_count = 0
        
        try:
            for filename in os.listdir(self.log_dir):
                if filename.endswith('.log'):
                    file_path = os.path.join(self.log_dir, filename)
                    if os.path.getmtime(file_path) < cutoff_time:
                        os.remove(file_path)
                        deleted_count += 1
        except Exception:
            pass
        
        return deleted_count

# Instance globale du logger
logger = TunisiaTourLogger()

def get_logger():
    """
    Obtient l'instance du logger
    
    Returns:
        Instance de TunisiaTourLogger
    """
    return logger

# Décorateur pour logger les performances
def log_performance(operation_name: str):
    """
    Décorateur pour logger les performances d'une fonction
    
    Args:
        operation_name: Nom de l'opération
    """
    def decorator(func):
        import time
        
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                logger.error(f"Error in {operation_name}: {str(e)}")
                raise
            finally:
                duration = time.time() - start_time
                logger.log_performance(operation_name, duration, success)
        
        return wrapper
    return decorator 