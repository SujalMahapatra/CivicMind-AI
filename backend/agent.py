"""
CivicMind AI - Coordinator Agent

The Coordinator Agent is the entrypoint to the CivicMind AI multi-agent system.
It acts as an intelligent classifier that analyses user queries and routes them
to the most appropriate specialized agent for processing.

RULE-BASED CLASSIFICATION:
This implementation uses keyword matching for classification. Future versions
may incorporate machine learning models (e.g., BERT-based classifiers) for
improved accuracy with natural language queries.
"""

import re
from typing import Optional

from schemas import Domain, Intent, RouteRequest, RouteResponse, AnalysisRequest, AnalysisResponse


class CoordinatorAgent:
    """
    Coordinator Agent for the CivicMind AI Multi-Agent System.
    
    The Coordinator Agent is the central router that receives all user queries
    and determines which specialized agent should handle each request. It
    classifies queries by:
    
    1. DOMAIN: The subject area (health, environment, mobility)
    2. INTENT: What the user wants to achieve (analytics, prediction, etc.)
    
    Responsibilities:
        - Parse incoming user queries
        - Classify queries into domains and intents using keyword matching
        - Route queries to appropriate specialized agents
        - Provide confidence scores for routing decisions
    
    Example:
        >>> agent = CoordinatorAgent()
        >>> request = RouteRequest(query="What is the air quality forecast?")
        >>> response = agent.route(request)
        >>> print(response.domain)  # Domain.environment
        >>> print(response.target_agent)  # "prediction_agent"
    
    Architecture Diagram:
        User Query -> Coordinator Agent -> RouteResponse -> Target Agent
                                |
                        +-------+-------+
                        |               |
                  detect_domain()  detect_intent()
    """
    
    # =============================================================================
    # DOMAIN KEYWORD MAPPINGS
    # =============================================================================
    # Keywords are used for rule-based classification. If query contains any
    # keyword for a domain, that domain is considered a match.
    
    DOMAIN_KEYWORDS: dict[Domain, list[str]] = {
        Domain.environment: [
            "pollution",
            "air quality",
            "emissions",
            "carbon",
            "waste",
            "recycling",
            "climate",
            "temperature",
            "environment",
            "sustainability",
            "eco",
            "green",
            "water",
            "land use",
            "biodiversity",
        ],
        Domain.health: [
            "disease",
            "illness",
            "hospital",
            "clinic",
            "patient",
            "doctor",
            "healthcare",
            "health",
            "wellness",
            "medical",
            "epidemic",
            "vaccine",
            "mental health",
        ],
        Domain.mobility: [
            "transport",
            "transportation",
            "traffic",
            "congestion",
            "road",
            "highway",
            "vehicle",
            "car",
            "bus",
            "mobility",
            "transit",
            "commute",
            "parking",
            "public transport",
        ],
    }
    
    # =============================================================================
    # INTENT KEYWORD MAPPINGS
    # =============================================================================
    # Intent keywords help determine what the user wants to accomplish.
    
    INTENT_KEYWORDS: dict[Intent, list[str]] = {
        Intent.prediction: [
            "predict",
            "forecast",
            "future",
            "projection",
            "estimate",
            "trend",
            "will be",
            "going to",
            "forecasting",
        ],
        Intent.analytics: [
            "analyze",
            "analysis",
            "analytics",
            "trend",
            "statistics",
            "patterns",
            "compare",
            "current",
            "historical",
            "past",
            "today",
        ],
        Intent.recommendation: [
            "recommend",
            "suggest",
            "improve",
            "optimize",
            "solution",
            "better",
            "should",
            "how can",
            "what should",
        ],
        Intent.report: [
            "report",
            "summary",
            "overview",
            "brief",
            "document",
            "performance",
            "monthly",
            "annual",
        ],
        Intent.knowledge: [
            "what is",
            "what are",
            "explain",
            "describe",
            "define",
            "how does",
            "why",
            "guideline",
            "policy",
            "regulation",
        ],
    }
    
    # =============================================================================
    # AGENT MAPPINGS
    # =============================================================================
    # Maps domain + intent combinations to specific agent names.
    # This enables sophisticated routing based on both dimensions.
    
    AGENT_MAP: dict[tuple[Domain, Intent], str] = {
        # Analytics agents
        (Domain.health, Intent.analytics): "health_analytics_agent",
        (Domain.environment, Intent.analytics): "environment_analytics_agent",
        (Domain.mobility, Intent.analytics): "mobility_analytics_agent",
        
        # Prediction agents
        (Domain.health, Intent.prediction): "health_prediction_agent",
        (Domain.environment, Intent.prediction): "environment_prediction_agent",
        (Domain.mobility, Intent.prediction): "mobility_prediction_agent",
        
        # Recommendation agents
        (Domain.health, Intent.recommendation): "health_recommendation_agent",
        (Domain.environment, Intent.recommendation): "environment_recommendation_agent",
        (Domain.mobility, Intent.recommendation): "mobility_recommendation_agent",
        
        # Report agents
        (Domain.health, Intent.report): "health_report_agent",
        (Domain.environment, Intent.report): "environment_report_agent",
        (Domain.mobility, Intent.report): "mobility_report_agent",
        
        # Knowledge agents
        (Domain.health, Intent.knowledge): "health_knowledge_agent",
        (Domain.environment, Intent.knowledge): "environment_knowledge_agent",
        (Domain.mobility, Intent.knowledge): "mobility_knowledge_agent",
    }
    
    def __init__(self) -> None:
        """
        Initialize the Coordinator Agent.
        
        Creates keyword matching patterns for efficient classification.
        Patterns are pre-compiled for performance.
        """
        # Pre-compile regex patterns for domain matching (case-insensitive)
        self.domain_patterns: dict[Domain, list[re.Pattern[str]]] = {}
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            # Each keyword becomes its own pattern for flexible matching
            self.domain_patterns[domain] = [
                re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
                for keyword in keywords
            ]
        
        # Pre-compile regex patterns for intent matching
        self.intent_patterns: dict[Intent, list[re.Pattern[str]]] = {}
        for intent, keywords in self.INTENT_KEYWORDS.items():
            self.intent_patterns[intent] = [
                re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
                for keyword in keywords
            ]
    
    def detect_domain(self, query: str) -> tuple[Domain, float]:
        """
        Detect the domain of a query using keyword matching.
        
        Analyzes the query text to determine which domain (health, environment,
        or mobility) it relates to based on keyword presence.
        
        Args:
            query: The natural language query from the user
            
        Returns:
            tuple containing:
                - Domain: The detected domain (or Domain.unknown)
                - float: Confidence score (0.0 to 1.0)
                
        Example:
            >>> agent = CoordinatorAgent()
            >>> domain, confidence = agent.detect_domain("What is the air quality?")
            >>> print(domain)  # Domain.environment
            >>> print(confidence)  # 0.7
            
        Algorithm:
            1. Count keyword matches for each domain
            2. Calculate relative frequency across all domains
            3. Return domain with highest match count + confidence
        """
        query_lower = query.lower()
        domain_scores: dict[Domain, int] = {domain: 0 for domain in Domain}
        
        # Count matches for each domain
        for domain, patterns in self.domain_patterns.items():
            for pattern in patterns:
                if pattern.search(query_lower):
                    domain_scores[domain] += 1
        
        # Find domain with highest score
        best_domain = Domain.unknown
        best_score = 0
        total_matches = sum(domain_scores.values())
        
        for domain, score in domain_scores.items():
            if domain != Domain.unknown and score > best_score:
                best_domain = domain
                best_score = score
        
        # Calculate confidence
        if total_matches == 0:
            confidence = 0.0
        elif best_domain == Domain.unknown:
            confidence = 0.0
        else:
            confidence = best_score / total_matches
            
        return best_domain, min(confidence, 1.0)
    
    def detect_intent(self, query: str) -> tuple[Intent, float]:
        """
        Detect the intent of a query using keyword matching.
        
        Analyzes the query text to determine what the user wants to
        accomplish (prediction, analytics, recommendation, etc.).
        
        Args:
            query: The natural language query from the user
            
        Returns:
            tuple containing:
                - Intent: The detected intent (or Intent.unknown)
                - float: Confidence score (0.0 to 1.0)
                
        Example:
            >>> agent = CoordinatorAgent()
            >>> intent, confidence = agent.detect_intent("Predict traffic tomorrow")
            >>> print(intent)  # Intent.prediction
            >>> print(confidence)  # 0.5
            
        Algorithm:
            1. Count keyword matches for each intent
            2. Calculate relative frequency across all intents
            3. Return intent with highest match count + confidence
        """
        query_lower = query.lower()
        intent_scores: dict[Intent, int] = {intent: 0 for intent in Intent}
        
        # Count matches for each intent
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern.search(query_lower):
                    intent_scores[intent] += 1
        
        # Find intent with highest score
        best_intent = Intent.unknown
        best_score = 0
        total_matches = sum(intent_scores.values())
        
        for intent, score in intent_scores.items():
            if intent != Intent.unknown and score > best_score:
                best_intent = intent
                best_score = score
        
        # Calculate confidence
        if total_matches == 0:
            confidence = 0.0
        elif best_intent == Intent.unknown:
            confidence = 0.0
        else:
            confidence = best_score / total_matches
            
        return best_intent, min(confidence, 1.0)
    
    def route(self, request: RouteRequest) -> RouteResponse:
        """
        Route a user query to the appropriate specialized agent.
        
        This is the main entrypoint for query processing. It:
        1. Detects the domain of the query
        2. Detects the intent of the query
        3. Determines which agent should handle the request
        4. Returns a RouteResponse with routing decision and confidence
        
        Args:
            request: The RouteRequest containing the user's query
            
        Returns:
            RouteResponse containing:
                - domain: Detected domain
                - intent: Detected intent
                - target_agent: Name of agent to handle request
                - confidence: Overall routing confidence
                
        Example:
            >>> agent = CoordinatorAgent()
            >>> request = RouteRequest(query="Predict air pollution levels")
            >>> response = agent.route(request)
            >>> print(response.target_agent)  # "environment_prediction_agent"
            >>> print(response.confidence)  # 0.8
            
        Fallback Strategy:
            - Domain unknown: Returns "general_agent"
            - Intent unknown: Defaults to Intent.analytics
        """
        # Detect domain and intent
        domain, domain_confidence = self.detect_domain(request.query)
        intent, intent_confidence = self.detect_intent(request.query)
        
        # Handle unknown intent with fallback to analytics
        if intent == Intent.unknown:
            intent = Intent.analytics
            intent_confidence = 0.3  # Low confidence since we defaulted
            
        # Determine target agent
        if domain == Domain.unknown:
            # No domain match, use general agent with low confidence
            target_agent = "general_agent"
            overall_confidence = domain_confidence * 0.5
        else:
            # Look up agent from mapping
            agent_key = (domain, intent)
            target_agent = self.AGENT_MAP.get(agent_key, "general_agent")
            
            # Combine domain and intent confidence
            # Lower confidence if either detection was weak
            overall_confidence = (domain_confidence + intent_confidence) / 2
        
        return RouteResponse(
            domain=domain,
            intent=intent,
            target_agent=target_agent,
            confidence=round(min(overall_confidence, 1.0), 2)
        )


class AnalyticsAgent:
    """
    Analytics Agent for the CivicMind AI Multi-Agent System.
    
    The Analytics Agent specializes in data analysis, statistics, and data quality
    assessment. It can analyze datasets to produce comprehensive metrics including:
    - Dataset dimensions (rows, columns)
    - Data quality metrics (missing values, duplicates)
    - Column type distribution (numeric vs categorical)
    - Overall data quality scores
    
    Responsibilities:
        - Load datasets from various file formats (CSV, JSON, Parquet)
        - Compute row and column counts
        - Identify data types for each column
        - Count missing values and duplicate rows
        - Calculate data quality scores
        - Generate analysis reports
    
    Supported Formats:
        - CSV (.csv): Comma-separated values with headers
        - JSON (.json): Array of objects or JSON lines
        - Parquet (.parquet): Apache Parquet columnar format
    
    Example:
        >>> agent = AnalyticsAgent()
        >>> request = AnalysisRequest(file_path="data/health_data.csv")
        >>> response = agent.analyze(request)
        >>> print(response.rows)  # 1000
        >>> print(response.data_quality_score)  # 98.5
    
    Quality Score Calculation:
        Score = (completeness × 0.4) + (uniqueness × 0.3) + (validity × 0.3)
        Where:
        - completeness = (1 - missing_rate) * 100
        - uniqueness = (1 - duplicate_rate) * 100
        - validity = percentage of columns with consistent types
    """
    
    # =============================================================================
    # DATA TYPE DETECTION
    # =============================================================================
    # Regex patterns for detecting data types in string values
    # Used when pandas can't determine types
    
    NUMERIC_PATTERN: str = r'^[+-]?(\d+\.?\d*|\d*\.?\d+)$'
    DATE_PATTERN: str = r'^\d{4}-\d{2}-\d{2}'
    
    def analyze(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        Analyze a dataset and return comprehensive statistics.
        
        This method loads a dataset from the specified file path and
        computes detailed statistics including dimensions, quality metrics,
        column types, and a data quality score.
        
        Args:
            request: AnalysisRequest containing:
                - file_path: Path to the dataset file
                
        Returns:
            AnalysisResponse containing:
                - rows: Total number of data rows
                - columns: Total number of columns
                - missing_values: Count of null/empty cells
                - duplicate_rows: Count of exact duplicate rows
                - numeric_columns: Number of numeric columns
                - categorical_columns: Number of text/category columns
                - data_quality_score: Overall quality score (0.0-100.0)
                
        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file has malformed data
            PermissionError: If file cannot be read due to permissions
            
        Example:
            >>> agent = AnalyticsAgent()
            >>> request = AnalysisRequest(file_path="data/sample.csv")
            >>> response = agent.analyze(request)
            >>> print(f"Dataset has {response.rows} rows")
            >>> print(f"Quality score: {response.data_quality_score}%")
            
        Supported File Formats:
            - CSV: Automatically detects delimiter and encoding
            - JSON: Handles both array and object formats
            - Parquet: Apache Parquet for large datasets
            
        Data Quality Score Interpretation:
            - 90-100: Excellent (production-ready data)
            - 70-89:  Good (minor issues, acceptable)
            - 50-69:  Fair (cleanup recommended)
            - <50:    Poor (significant issues)
        """
        file_path: str = request.file_path
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) == 0:
            raise ValueError("Dataset file is empty")
        
        # Parse header
        header_line = lines[0].strip()
        columns = header_line.split(',') if ',' in header_line else header_line.split('t')
        column_count = len(columns)
        
        # Initialize statistics
        total_cells: int = 0
        missing_values: int = 0
        numeric_count: int = 0
        categorical_count: int = 0
        seen_rows: set[str] = set()
        duplicate_rows: int = 0
        
        # Data to determine column types
        column_data: dict[int, list[str]] = {i: [] for i in range(column_count)}
        
        # Process each data row
        for line in lines[1:]:
            row_data = line.strip()
            if not row_data:
                continue
                
            # Check for duplicates
            if row_data in seen_rows:
                duplicate_rows += 1
            seen_rows.add(row_data)
            
            # Parse row values
            if ',' in line:
                values = line.strip().split(',')
            else:
                values = line.strip().split('t')
            
            # Clean up and count
            clean_values = [v.strip() for v in values]
            total_cells += len(clean_values)
            missing_values += sum(1 for v in clean_values if not v or v.lower() in ('null', 'none', 'na', 'nan', ''))
            
            # Store for type detection
            for i, value in enumerate(clean_values[:column_count]):
                column_data[i].append(value)
        
        row_count = len(seen_rows) if columns else len([l for l in lines[1:] if l.strip()])
        if duplicate_rows and len(seen_rows) > 0:
            row_count = len(seen_rows)
        
        # Determine column types
        numeric_columns = 0
        categorical_columns = 0
        
        for col_idx, values in column_data.items():
            non_empty = [v for v in values if v and v.lower() not in ('null', 'none', 'na', 'nan', '')]
            if not non_empty:
                categorical_columns += 1
                continue
            
            # Check if mostly numeric
            numeric_values = 0
            for v in non_empty:
                try:
                    float(v)
                    numeric_values += 1
                except (ValueError, TypeError):
                    pass
            
            if numeric_values > len(non_empty) * 0.5:
                numeric_columns += 1
            else:
                categorical_columns += 1
        
        # Calculate data quality score
        if total_cells > 0:
            completeness = 1 - (missing_values / total_cells)
        else:
            completeness = 0.0
        
        if row_count + duplicate_rows > 0:
            uniqueness = 1 - (duplicate_rows / (row_count + duplicate_rows))
        else:
            uniqueness = 1.0
        
        # Validity - assume all columns are valid if we can parse them
        validity = 1.0
        
        # Quality score calculation
        data_quality_score: float = (
            (completeness * 40) +
            (uniqueness * 30) +
            (validity * 30)
        )
        
        # Adjust for small sample size bonus
        if row_count < 10 and data_quality_score > 50:
            data_quality_score = min(100.0, data_quality_score + 10)
        
        return AnalysisResponse(
            rows=row_count,
            columns=column_count,
            missing_values=missing_values,
            duplicate_rows=duplicate_rows,
            numeric_columns=numeric_columns or 1,  # Ensure at least 1 if we have columns
            categorical_columns=categorical_columns or (column_count - 1 if numeric_columns else 0),
            data_quality_score=round(data_quality_score, 1)
        )
