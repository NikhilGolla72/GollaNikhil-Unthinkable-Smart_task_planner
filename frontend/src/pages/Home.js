import React, { useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [goal, setGoal] = useState("");
  const [teamSize, setTeamSize] = useState(1);
  const [mode, setMode] = useState("balanced");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const submit = async () => {
    if (!goal.trim()) {
      setError("Please enter a goal");
      return;
    }
    
    setLoading(true);
    setError("");
    
    try {
        const res = await axios.post("http://localhost:8001/api/generate_plan", {
          goal: goal.trim(),
          team_size: teamSize,
          mode
        });
      
      // Navigate to planner view with the generated plan
      navigate(`/planner/${res.data.plan_id}`, { state: { planData: res.data } });
    } catch (e) {
      setError("Error: " + (e.response?.data?.detail || e.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl mx-auto"
        >
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-4">
              Smart Task Planner
            </h1>
            <p className="text-xl text-gray-600">
              AI-Powered Goal-to-Plan Generator
            </p>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-white rounded-lg shadow-xl p-8"
          >
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Goal Description *
                </label>
                <textarea
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  placeholder="e.g., Build an MVP for Smart Task Planner in 10 days"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Team Size
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="20"
                    value={teamSize}
                    onChange={(e) => setTeamSize(Number(e.target.value))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Planning Mode
                  </label>
                  <select
                    value={mode}
                    onChange={(e) => setMode(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="balanced">Balanced</option>
                    <option value="aggressive">Aggressive</option>
                    <option value="safe">Safe</option>
                  </select>
                </div>
              </div>

              {error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg"
                >
                  {error}
                </motion.div>
              )}

              <motion.button
                onClick={submit}
                disabled={loading}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Generating Plan...
                  </div>
                ) : (
                  "Generate Smart Plan"
                )}
              </motion.button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="mt-8 text-center"
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-lg">
                <div className="text-blue-600 text-2xl mb-2">🎯</div>
                <h3 className="font-semibold text-gray-800 mb-2">Smart Breakdown</h3>
                <p className="text-gray-600 text-sm">AI-powered task decomposition with dependency mapping</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-lg">
                <div className="text-green-600 text-2xl mb-2">📊</div>
                <h3 className="font-semibold text-gray-800 mb-2">Multiple Strategies</h3>
                <p className="text-gray-600 text-sm">Balanced, aggressive, and safe planning approaches</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-lg">
                <div className="text-purple-600 text-2xl mb-2">⚡</div>
                <h3 className="font-semibold text-gray-800 mb-2">Visual Timeline</h3>
                <p className="text-gray-600 text-sm">Interactive Gantt charts with critical path analysis</p>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
