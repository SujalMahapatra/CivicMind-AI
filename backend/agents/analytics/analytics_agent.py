"""
CivicMind AI - Analytics Agent

This module provides the Analytics Agent implementation for the CivicMind AI
platform. The Analytics Agent specializes in data analysis, statistics, and
quality assessment for community datasets.

PURPOSE:
    The Analytics Agent loads datasets, computes descriptive statistics,
    identifies data quality issues, and generates comprehensive profiles
    that help users understand their data before making decisions.

SUPPORTED FORMATS:
    - CSV (.csv): Comma-separated values with headers
    - Excel (.xlsx): Microsoft Excel spreadsheets
    - JSON (.json): JavaScript Object Notation files

ARCHITECTURE:
    The agent follows clean architecture principles:
    - Single Responsibility: Each method has one purpose
    - Dependency Injection: Accepts file paths, returns typed responses
    - Error Handling: Meaningful exceptions with context
    - Pure Functions: No side effects, testable logic

DEPENDENCIES:
    - pandas: Data manipulation and analysis
    - numpy: Numerical operations
    - pathlib: Cross-platform file path handling
"""


from pathlib import Path
from typing import Set


import pandas as pd
import numpy as np

from .schemas import AnalysisResponse

class AnalyticsAgent:
    """
    Analytics Agent for CivicMind AI Multi-Agent System.
    
    The Analytics Agent specializes in dataset loading, statistical analysis,
    and data quality assessment. It can handle multiple file formats and
    provides comprehensive insights into dataset structure and quality.
    
    Core Capabilities:
        - Multi-format dataset loading (CSV, XLSX, JSON)
        - Column type detection (numeric vs categorical)
        - Missing value and duplicate detection
        - Data quality scoring (0-100 scale)
        - Statistical profiling
    
    Data Quality Score Formula:
        - Base score: 100 points
        - Missing value penalty: Missing percentage * 50
        - Duplicate penalty: Duplicate percentage * 25
        - Score clamped between 0 and 100
    
    Example Usage:
        >>> agent = AnalyticsAgent()
        >>> response = agent.analyze("datasets/health_data.csv")
        >>> print(f"Quality Score: {response.data_quality_score}%")
        >>> print(f"Dataset: {response.rows} rows x {response.columns} columns")
    
    Error Handling:
        - FileNotFoundError: When file does not exist
        - ValueError: When file format is invalid or corrupted
        - PermissionError: When file cannot be read
    """
    
    # =============================================================================
    # CONSTANTS
    # =============================================================================
    # These constants define the data quality penalty multipliers.
    # They control how severely missing values and duplicates impact the score.
    
    MISSING_PENALTY_MULTIPLIER: float = 50.0
    DUPLICATE_PENALTY_MULTIPLIER: float = 25.0
    MAX_QUALITY_SCORE: float = 100.0
    MIN_QUALITY_SCORE: float = 0.0
    
    # File type detection patterns
    SUPPORTED_EXTENSIONS: Set[str] = {'.csv', '.xlsx', '.json'}
    
    def __init__(self) -> None:
        """
        Initialize the Analytics Agent.
        
        Creates a new AnalyticsAgent instance ready to process datasets.
        The agent maintains no state between analyses, making it thread-safe
        and reusable for multiple datasets.
        
        Example:
            >>> agent = AnalyticsAgent()
            >>> # Agent is now ready to analyze datasets
        """
        pass
    
    def load_dataset(self, file_path: str) -> pd.DataFrame:
        """
        Load a dataset file into a pandas DataFrame.
        
        This method automatically detects the file format based on the
        file extension and uses the appropriate pandas reader function.
        It handles CSV, Excel (XLS/XLSX), and JSON formats.
        
        Args:
            file_path: Path to the dataset file. Can be relative or absolute.
        
        Returns:
            pd.DataFrame: Loaded dataset with all columns and rows.
            
        Raises:
            FileNotFoundError: If the file does not exist at the path
            ValueError: If the file format is unsupported or corrupted
            PermissionError: If the file cannot be read due to permissions
            
        Example:
            >>> agent = AnalyticsAgent()
            >>> df = agent.load_dataset("datasets/sample.csv")
            >>> print(df.head())
            
        Supported Formats:
            - .csv: Comma-separated values (auto-detects delimiter)
            - .xlsx: Microsoft Excel spreadsheets
            - .json: JSON array of objects or JSON lines format
        """
        # Convert string path to Path object for cross-platform compatibility
        # pathlib handles Windows backslashes vs Unix forward slashes
        path_obj = Path(file_path)
        
        # VALIDATION: Check file exists before attempting to load
        if not path_obj.exists():
            raise FileNotFoundError(
                f"Dataset file not found: '{file_path}'. "
                f"Please verify the path and try again."
            )
        
        # VALIDATION: Ensure path points to a file, not a directory
        if not path_obj.is_file():
            raise ValueError(
                f"Path is not a file: '{file_path}'. "
                f"Expected a dataset file (CSV, XLSX, or JSON)."
            )
        
        # Get file extension for format detection (lowercase for consistency)
        file_extension = path_obj.suffix.lower()
        
        # VALIDATION: Check if file format is supported
        if file_extension not in self.SUPPORTED_EXTENSIONS:
            supported = ', '.join(self.SUPPORTED_EXTENSIONS)
            raise ValueError(
                f"Unsupported file format: '{file_extension}'. "
                f"Supported formats: {supported}"
            )
        
        try:
            # DYNAMIC DISPATCH: Call appropriate loader based on extension
            if file_extension == '.csv':
                return self._load_csv(path_obj)
            elif file_extension == '.xlsx':
                return self._load_excel(path_obj)
            elif file_extension == '.json':
                return self._load_json(path_obj)
            else:
                # Should never reach here due to earlier validation
                raise ValueError(f"Unexpected file format: {file_extension}")
                
        except pd.errors.EmptyDataError:
            raise ValueError(
                f"Dataset file is empty: '{file_path}'. "
                f"Please provide a file with data."
            )
        except pd.errors.ParserError as e:
            raise ValueError(
                f"Failed to parse dataset file: '{file_path}'. "
                f"Error: {str(e)}. Please check file format."
            )
        except PermissionError:
            raise PermissionError(
                f"Permission denied reading file: '{file_path}'. "
                f"Check file permissions and try again."
            )
        except Exception as e:
            raise ValueError(
                f"Unexpected error loading dataset: '{file_path}'. "
                f"Error: {str(e)}"
            )
    
    def _load_csv(self, path: Path) -> pd.DataFrame:
        """
        Load a CSV file into a DataFrame.
        
        Pandas automatically detects delimiters (comma, semicolon, tab)
        and handles common CSV variations.
        
        Args:
            path: Path object pointing to CSV file
            
        Returns:
            pd.DataFrame: Loaded CSV data
        """
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin1")
    
    def _load_excel(self, path: Path) -> pd.DataFrame:
        """
        Load an Excel file (.xlsx) into a DataFrame.
        
        Reads the first sheet by default. For multi-sheet files,
        consider extending this method to accept sheet_name parameter.
        
        Args:
            path: Path object pointing to Excel file
            
        Returns:
            pd.DataFrame: Loaded Excel data from first sheet
        """
        return pd.read_excel(path)
    
    def _load_json(self, path: Path) -> pd.DataFrame:
        """
        Load a JSON file into a DataFrame.
        
        Supports:
        - Array of objects: [{"col1": 1}, {"col1": 2}]
        - Nested objects (flattens automatically)
        
        Args:
            path: Path object pointing to JSON file
            
        Returns:
            pd.DataFrame: Loaded JSON data
        """
        return pd.read_json(path)
    
    def calculate_data_quality_score(
        self,
        df: pd.DataFrame
    ) -> float:
        """
        Calculate a data quality score for a DataFrame.
        
        The quality score represents the overall health of the dataset,
        considering completeness (missing values) and uniqueness (duplicates).
        Perfect data has a score of 100.0, severely corrupted data approaches 0.0.
        
        Formula:
            - Base score: 100.0
            - Missing penalty: (missing_percentage * 50)
            - Duplicate penalty: (duplicate_percentage * 25)
            - Score = base_score - missing_penalty - duplicate_penalty
            - Score clamped between 0 and 100
        
        Why these weights:
            - Missing values are penalized more heavily (50x) because they
              directly reduce analysis accuracy and completeness
            - Duplicates are penalized less (25x) because they inflate
              statistics but don't necessarily corrupt the underlying data
        
        Args:
            df: The pandas DataFrame to score
            
        Returns:
            float: Quality score between 0.0 and 100.0
            
        Example:
            >>> agent = AnalyticsAgent()
            >>> df = pd.DataFrame({'a': [1, 2, None], 'b': [4, 5, 6]})
            >>> score = agent.calculate_data_quality_score(df)
            >>> print(f"Quality: {score:.1f}%")  # Handles one missing value
            
        Edge Cases:
            - Empty DataFrame: Returns 100.0 (technically perfect but empty)
            - All missing values: Approaches 0.0
            - All duplicates: Score reduced by 25 points minimum
        """
        # Handle edge case: empty DataFrame has perfect quality
        if df.empty:
            return self.MAX_QUALITY_SCORE
        
        # Get dataset dimensions for calculations
        total_rows: int = len(df)
        total_cells: int = total_rows * len(df.columns)
        
        # Calculate missing value metrics
        missing_count: int = df.isnull().sum().sum()  # Sum of all nulls
        missing_percentage: float = (
            missing_count / total_cells if total_cells > 0 else 0.0
        )
        
        # Calculate duplicate metrics
        # Note: drop_duplicates() returns a copy without duplicates
        duplicate_count = int(df.duplicated().sum())
        duplicate_percentage: float = (
            duplicate_count / total_rows if total_rows > 0 else 0.0
        )
        
        # BASE SCORE: Start with perfect score
        score: float = self.MAX_QUALITY_SCORE
        
        # APPLY PENALTIES
        # Missing values penalty (weighted 50x)
        score -= missing_percentage * self.MISSING_PENALTY_MULTIPLIER
        
        # Duplicate rows penalty (weighted 25x)
        score -= duplicate_percentage * self.DUPLICATE_PENALTY_MULTIPLIER
        
        # CLAMP: Ensure score stays within valid range [0, 100]
        # np.clip is cleaner than manual if/else chaining
        return float(np.clip(score, self.MIN_QUALITY_SCORE, self.MAX_QUALITY_SCORE))
    
    def analyze(self, file_path: str) -> AnalysisResponse:
        """
        Perform comprehensive analysis on a dataset file.
        
        This is the main entrypoint for dataset analysis. It:
        1. Loads the dataset from the specified path
        2. Computes row and column counts
        3. Counts missing values and duplicates
        4. Detects column types (numeric vs categorical)
        5. Calculates overall data quality score
        6. Returns structured response with all metrics
        
        Args:
            file_path: Path to the dataset file to analyze
            
        Returns:
            AnalysisResponse: Structured analysis results containing:
                - rows: Total data rows
                - columns: Total features
                - missing_values: Null/empty cell count
                - duplicate_rows: Duplicate row count
                - numeric_columns: Numeric column count
                - categorical_columns: Text/category column count
                - data_quality_score: Overall quality (0-100)
                
        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file is corrupted or unsupported format
            PermissionError: If file cannot be read
            
        Example:
            >>> agent = AnalyticsAgent()
            >>> response = agent.analyze("data/health_data.csv")
            >>> print(f"Dataset: {response.rows} rows")
            >>> print(f"Quality: {response.data_quality_score}%")
            
        Performance:
            - CSV: Fast for files up to ~1GB
            - Excel: Slower, better for <100MB files
            - JSON: Depends on nesting depth and structure
        """
        # STEP 1: Load dataset (raises exceptions on failure)
        df: pd.DataFrame = self.load_dataset(file_path)
        
        # STEP 2: Calculate basic dimensions
        rows: int = len(df)
        columns: int = len(df.columns)
        
        # STEP 3: Calculate data quality metrics
        missing_values: int = int(df.isnull().sum().sum())
        duplicate_rows: int = int(df.duplicated().sum())
        
        # STEP 4: Detect column types
        # Pandas dtypes classify columns as numeric (int64, float64), categorical, etc.
        numeric_columns: int = 0
        categorical_columns: int = 0
        
        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                numeric_columns += 1
            else:
                # Categorical includes: object, string, bool, datetime, etc.
                categorical_columns += 1
        
        # STEP 5: Calculate overall quality score
        data_quality_score: float = self.calculate_data_quality_score(df)

        # STEP 6: Extract file name from path for response
        file_name = Path(file_path).name
        
        # STEP 6: Return structured response
        return AnalysisResponse(
            rows=rows,
            columns=columns,
            missing_values=missing_values,
            duplicate_rows=duplicate_rows,
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            data_quality_score=round(data_quality_score, 1),
            file_name=file_name
            
        )
