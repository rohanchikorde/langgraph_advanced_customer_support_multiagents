import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

class AgentMemory:
    def __init__(self, storage_path: str = "data/agent_memory.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(exist_ok=True)
        self.memory = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from persistent storage"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: Corrupted memory file, starting fresh")
        return {
            "user_profiles": {},
            "successful_patterns": {},
            "knowledge_base": {},
            "stats": {"total_conversations": 0, "resolved_issues": 0}
        }

    def _save_memory(self):
        """Save memory to persistent storage"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=2, default=str)

    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get or create user profile"""
        if user_id not in self.memory["user_profiles"]:
            self.memory["user_profiles"][user_id] = {
                "conversation_history": [],
                "preferences": {},
                "resolved_issues": [],
                "common_issues": {},
                "last_interaction": None,
                "total_interactions": 0
            }
        return self.memory["user_profiles"][user_id]

    def save_conversation(self, user_id: str, conversation_data: Dict[str, Any]):
        """Save conversation data to user profile"""
        profile = self.get_user_profile(user_id)

        # Add conversation summary
        conversation_summary = {
            "timestamp": datetime.now().isoformat(),
            "query": conversation_data.get("query", ""),
            "categories": conversation_data.get("categories", []),
            "resolution": conversation_data.get("satisfactory", False),
            "response": conversation_data.get("response", ""),
            "entities": conversation_data.get("entities", {})
        }

        profile["conversation_history"].append(conversation_summary)
        profile["last_interaction"] = conversation_summary["timestamp"]
        profile["total_interactions"] += 1

        # Keep only last 50 conversations to prevent memory bloat
        if len(profile["conversation_history"]) > 50:
            profile["conversation_history"] = profile["conversation_history"][-50:]

        # Update common issues
        for category in conversation_summary["categories"]:
            profile["common_issues"][category] = profile["common_issues"].get(category, 0) + 1

        # If resolved, add to successful patterns
        if conversation_summary["resolution"]:
            self._add_successful_pattern(conversation_data)
            profile["resolved_issues"].append(conversation_summary)

        self.memory["stats"]["total_conversations"] += 1
        if conversation_summary["resolution"]:
            self.memory["stats"]["resolved_issues"] += 1

        self._save_memory()

    def _add_successful_pattern(self, conversation_data: Dict[str, Any]):
        """Add successful resolution pattern"""
        query = conversation_data.get("query", "").lower()
        categories = conversation_data.get("categories", [])
        categories_str = "_".join(sorted(categories))
        response = conversation_data.get("response", "")

        # Create pattern key using string
        pattern_key = f"{categories_str}_{hash(query) % 10000}"

        if pattern_key not in self.memory["successful_patterns"]:
            self.memory["successful_patterns"][pattern_key] = {
                "categories": categories,
                "query_patterns": [query],
                "successful_responses": [response],
                "frequency": 1,
                "last_used": datetime.now().isoformat()
            }
        else:
            pattern = self.memory["successful_patterns"][pattern_key]
            pattern["query_patterns"].append(query)
            pattern["successful_responses"].append(response)
            pattern["frequency"] += 1
            pattern["last_used"] = datetime.now().isoformat()

            # Keep only top 5 similar queries and responses
            pattern["query_patterns"] = pattern["query_patterns"][-5:]
            pattern["successful_responses"] = pattern["successful_responses"][-5:]

    def find_similar_past_issues(self, user_id: str, current_query: str, categories: List[str]) -> List[Dict[str, Any]]:
        """Find similar past issues for the user"""
        profile = self.get_user_profile(user_id)
        similar_issues = []

        current_words = set(current_query.lower().split())
        current_categories = set(categories)

        for issue in profile["conversation_history"]:
            # Check category overlap
            issue_categories = set(issue.get("categories", []))
            category_overlap = len(current_categories & issue_categories)

            # Check query similarity (simple word overlap)
            issue_words = set(issue.get("query", "").lower().split())
            word_overlap = len(current_words & issue_words)

            if category_overlap > 0 or word_overlap > 2:  # At least some similarity
                similarity_score = category_overlap * 2 + word_overlap
                similar_issues.append({
                    **issue,
                    "similarity_score": similarity_score
                })

        # Return top 3 most similar issues
        return sorted(similar_issues, key=lambda x: x["similarity_score"], reverse=True)[:3]

    def get_knowledge_base_entry(self, categories: List[str]) -> Optional[Dict[str, Any]]:
        """Get relevant knowledge base entry for categories"""
        categories_key = "_".join(sorted(categories))

        # Look for exact category match first
        if categories_key in self.memory["knowledge_base"]:
            return self.memory["knowledge_base"][categories_key]

        # Look for partial matches
        for kb_key, entry in self.memory["knowledge_base"].items():
            if any(cat in kb_key for cat in categories):
                return entry

        return None

    def update_knowledge_base(self, categories: List[str], query: str, resolution: str):
        """Update knowledge base with successful resolution"""
        categories_key = "_".join(sorted(categories))

        if categories_key not in self.memory["knowledge_base"]:
            self.memory["knowledge_base"][categories_key] = {
                "categories": list(categories_key.split("_")),
                "common_queries": [],
                "resolutions": [],
                "frequency": 0,
                "last_updated": datetime.now().isoformat()
            }

        kb_entry = self.memory["knowledge_base"][categories_key]
        kb_entry["common_queries"].append(query)
        kb_entry["resolutions"].append(resolution)
        kb_entry["frequency"] += 1
        kb_entry["last_updated"] = datetime.now().isoformat()

        # Keep only recent entries
        kb_entry["common_queries"] = kb_entry["common_queries"][-10:]
        kb_entry["resolutions"] = kb_entry["resolutions"][-10:]

        self._save_memory()

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        return self.memory["stats"]

# Global memory instance
agent_memory = AgentMemory()