"""
Table formatter for pretty output display.
"""

from typing import Dict, Any, List


class TableFormatter:
    """Formats converter results into nice tables."""
    
    def format_multiple_results(self, results_list: List[Dict[str, Any]]) -> str:
        """Format multiple converter results."""
        if not results_list:
            return "Unable to convert input"
        
        formatted_sections = []
        
        for result in results_list:
            converter_name = result['converter_name']
            formats = result['formats']
            
            lines = []
            lines.append(f"{converter_name}:")
            lines.append("-" * len(f"{converter_name}:"))
            
            for key, value in formats.items():
                lines.append(f"{key}: {value}")
            
            formatted_sections.append("\n".join(lines))
        
        return "\n\n".join(formatted_sections)
