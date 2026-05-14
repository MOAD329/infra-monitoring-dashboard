def generate_recommendations(anomalies):
    recommendations = []

    for anomaly in anomalies:
        metric = anomaly["metric"]
        severity = anomaly["severity"]

        if metric == "cpu_usage":
            recommendations.append({
                "priorite": severity,
                "categorie": "Calcul / CPU",
                "probleme": "Utilisation CPU élevée",
                "explication": (
                    "Le serveur consomme une part importante de ses ressources CPU. "
                    "Cela peut indiquer une surcharge applicative, un traitement trop lourd, "
                    "ou un nombre trop important de requêtes simultanées."
                ),
                "action": (
                    "Identifier les processus les plus consommateurs, analyser les pics de charge, "
                    "optimiser le code applicatif si nécessaire, puis envisager une répartition de charge "
                    "ou un scaling horizontal."
                )
            })

        elif metric == "memory_usage":
            recommendations.append({
                "priorite": severity,
                "categorie": "Mémoire",
                "probleme": "Utilisation mémoire élevée",
                "explication": (
                    "La mémoire disponible devient limitée. Une consommation mémoire élevée peut provoquer "
                    "des ralentissements, des redémarrages de services ou une dégradation globale des performances."
                ),
                "action": (
                    "Analyser les services consommateurs de RAM, vérifier la présence de fuites mémoire, "
                    "optimiser la configuration applicative et augmenter la mémoire si la charge est normale."
                )
            })

        elif metric == "latency_ms":
            recommendations.append({
                "priorite": severity,
                "categorie": "Performance applicative",
                "probleme": "Latence élevée",
                "explication": (
                    "Le temps de réponse est supérieur au seuil acceptable. Cela peut venir d’un service lent, "
                    "d’une base de données sous charge, d’un réseau saturé ou d’un cache inefficace."
                ),
                "action": (
                    "Analyser les temps de réponse API, vérifier les requêtes lentes en base de données, "
                    "activer ou optimiser le cache, et contrôler la performance de l’API Gateway."
                )
            })

        elif metric == "disk_usage":
            recommendations.append({
                "priorite": severity,
                "categorie": "Stockage",
                "probleme": "Espace disque élevé",
                "explication": (
                    "Le disque approche d’un niveau d’utilisation important. Cela peut bloquer l’écriture "
                    "de logs, les sauvegardes ou certains traitements applicatifs."
                ),
                "action": (
                    "Nettoyer les fichiers temporaires, archiver les anciens logs, vérifier la rotation des logs "
                    "et prévoir une extension de capacité si la croissance est normale."
                )
            })

        elif metric == "io_wait":
            recommendations.append({
                "priorite": severity,
                "categorie": "Entrées / Sorties disque",
                "probleme": "Temps d’attente disque élevé",
                "explication": (
                    "Le système attend trop longtemps les opérations disque. Cela peut ralentir fortement "
                    "les services dépendants du stockage."
                ),
                "action": (
                    "Identifier les opérations disque intensives, optimiser les accès aux fichiers, "
                    "vérifier les performances du stockage et envisager un disque plus performant si nécessaire."
                )
            })

        elif metric == "temperature_celsius":
            recommendations.append({
                "priorite": severity,
                "categorie": "Matériel",
                "probleme": "Température serveur élevée",
                "explication": (
                    "La température du serveur est élevée. Une surchauffe peut provoquer une baisse automatique "
                    "des performances ou des arrêts de sécurité."
                ),
                "action": (
                    "Vérifier la ventilation, la température de la salle serveur, l’état du matériel "
                    "et réduire temporairement la charge si nécessaire."
                )
            })

        elif metric == "error_rate":
            recommendations.append({
                "priorite": severity,
                "categorie": "Fiabilité applicative",
                "probleme": "Taux d’erreur élevé",
                "explication": (
                    "Le taux d’erreur applicatif dépasse le seuil défini. Cela peut indiquer des bugs, "
                    "des erreurs de configuration ou une dépendance externe instable."
                ),
                "action": (
                    "Analyser les logs applicatifs, identifier les endpoints les plus touchés, "
                    "corriger les erreurs récurrentes et surveiller l’évolution après correction."
                )
            })

        elif metric.startswith("service_status"):
            recommendations.append({
                "priorite": severity,
                "categorie": "Disponibilité service",
                "probleme": "Service dégradé ou indisponible",
                "explication": (
                    "Un composant critique de l’infrastructure n’est pas dans un état pleinement opérationnel. "
                    "Cela peut impacter directement les utilisateurs ou d’autres services dépendants."
                ),
                "action": (
                    "Identifier le service concerné, consulter ses logs, vérifier ses dépendances, "
                    "redémarrer le composant si nécessaire et prévoir une stratégie de haute disponibilité."
                )
            })

    return recommendations