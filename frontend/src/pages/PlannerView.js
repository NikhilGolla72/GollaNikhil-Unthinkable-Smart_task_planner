import React, { useState, useEffect } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import axios from "axios";
import TaskCard from "../components/TaskCard";
import GanttChart from "../components/GanttChart";
import ModeSelector from "../components/ModeSelector";

export default function PlannerView() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [planData, setPlanData] = useState(null);
  const [selectedMode, setSelectedMode] = useState("balanced");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    // Check if plan data was passed via navigation state
    if (location.state?.planData) {
      setPlanData(location.state.planData);
      setLoading(false);
    } else {
      // If no data passed, could implement API call to fetch by ID
      setError("Plan data not found. Please generate a new plan.");
      setLoading(false);
    }
  }, [location.state, id]);

  const handleExportJSON = () => {
    if (planData) {
      const dataStr = JSON.stringify(planData, null, 2);
      const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
      const exportFileDefaultName = `smart-plan-${id}.json`;
      
      const linkElement = document.createElement('a');
      linkElement.setAttribute('href', dataUri);
      linkElement.setAttribute('download', exportFileDefaultName);
      linkElement.click();
    }
  };


  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your smart plan...</p>
        </div>
      </div>
    );
  }

  if (error || !planData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg mb-4">
            {error}
          </div>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  const currentVariant = planData.variants[selectedMode];
  const tasks = currentVariant.tasks || [];
  const criticalPath = currentVariant.critical_path || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-7xl mx-auto"
        >
          {/* Header */}
          <div className="bg-white rounded-lg shadow-xl p-6 mb-8">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-800 mb-2">
                  Smart Task Plan
                </h1>
                <p className="text-gray-600">Plan ID: {id}</p>
              </div>
              <button
                onClick={() => navigate('/')}
                className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
              >
                ← New Plan
              </button>
            </div>

            {planData.summary && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                <h3 className="font-semibold text-blue-800 mb-2">Plan Summary</h3>
                <p className="text-blue-700">{planData.summary}</p>
              </div>
            )}

            {planData.assumptions && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h3 className="font-semibold text-yellow-800 mb-2">Assumptions</h3>
                <p className="text-yellow-700">{planData.assumptions}</p>
              </div>
            )}
          </div>

          {/* Mode Selector */}
          <div className="bg-white rounded-lg shadow-xl p-6 mb-8">
            <ModeSelector mode={selectedMode} onChange={setSelectedMode} />
          </div>

          {/* Plan Analytics */}
          <div className="bg-white rounded-lg shadow-xl p-6 mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Plan Analytics</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {tasks.reduce((sum, task) => sum + task.est_hours, 0).toFixed(1)}h
                </div>
                <div className="text-sm text-blue-800">Total Hours</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{tasks.length}</div>
                <div className="text-sm text-green-800">Total Tasks</div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {(tasks.reduce((sum, task) => sum + task.risk_score, 0) / tasks.length || 0).toFixed(1)}
                </div>
                <div className="text-sm text-purple-800">Avg Risk</div>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-orange-600">{criticalPath.length}</div>
                <div className="text-sm text-orange-800">Critical Path</div>
              </div>
            </div>
          </div>

          {/* Reasoning */}
          {currentVariant.reasoning && (
            <div className="bg-white rounded-lg shadow-xl p-6 mb-8">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Planning Reasoning</h3>
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <p className="text-gray-700">{currentVariant.reasoning}</p>
              </div>
            </div>
          )}

          {/* Gantt Chart */}
          <div className="bg-white rounded-lg shadow-xl p-6 mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Timeline View</h3>
            <GanttChart tasks={tasks} criticalPath={criticalPath} />
          </div>

          {/* Task Cards */}
          <div className="bg-white rounded-lg shadow-xl p-6 mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Task Details</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tasks.map((task, index) => (
                <motion.div
                  key={task.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                >
                  <TaskCard 
                    task={task} 
                    isCritical={criticalPath.includes(task.id)}
                  />
                </motion.div>
              ))}
            </div>
          </div>

          {/* Export Options */}
          <div className="bg-white rounded-lg shadow-xl p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Export Options</h3>
            <div className="flex gap-4">
              <button
                onClick={handleExportJSON}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 flex items-center"
              >
                📄 Export JSON
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
