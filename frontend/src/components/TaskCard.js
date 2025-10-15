import React from "react";
import { motion } from "framer-motion";

export default function TaskCard({ task, isCritical = false }) {
  const getRiskColor = (riskScore) => {
    if (riskScore >= 4) return "bg-red-100 border-red-300 text-red-800";
    if (riskScore >= 3) return "bg-yellow-100 border-yellow-300 text-yellow-800";
    return "bg-green-100 border-green-300 text-green-800";
  };

  const getRiskText = (riskScore) => {
    if (riskScore >= 4) return "High Risk";
    if (riskScore >= 3) return "Medium Risk";
    return "Low Risk";
  };

  const formatDate = (dateString) => {
    if (!dateString) return "TBD";
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className={`bg-white border-2 rounded-lg p-4 shadow-lg transition-all duration-200 ${
        isCritical ? "border-red-400 bg-red-50" : "border-gray-200"
      }`}
    >
      {isCritical && (
        <div className="flex items-center mb-2">
          <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full font-semibold">
            CRITICAL PATH
          </span>
        </div>
      )}
      
      <div className="flex justify-between items-start mb-3">
        <h4 className="font-semibold text-gray-800 text-lg leading-tight">
          {task.title}
        </h4>
        <div className="text-right">
          <div className="text-lg font-bold text-blue-600">
            {task.est_hours}h
          </div>
          {task.team_member && task.team_size > 1 && (
            <div className="text-xs text-blue-600 font-semibold">
              Member {task.team_member}
            </div>
          )}
          {task.team_size && task.team_size > 1 && !task.team_member && (
            <div className="text-xs text-gray-500">
              Team: {task.team_size}
            </div>
          )}
        </div>
      </div>

      {task.description && (
        <p className="text-gray-600 text-sm mb-3 leading-relaxed">
          {task.description}
        </p>
      )}

      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getRiskColor(task.risk_score)}`}>
            {getRiskText(task.risk_score)}
          </span>
          <span className="text-xs text-gray-500">
            Risk: {task.risk_score}/5
          </span>
        </div>

        <div className="text-xs text-gray-500">
          <div className="flex justify-between">
            <span>Start: {formatDate(task.start)}</span>
            <span>End: {formatDate(task.end)}</span>
          </div>
        </div>

        {task.dependencies && task.dependencies.length > 0 && (
          <div className="mt-3">
            <div className="text-xs text-gray-500 mb-1">Dependencies:</div>
            <div className="flex flex-wrap gap-1">
              {task.dependencies.map((dep, index) => (
                <span
                  key={index}
                  className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
                >
                  {dep}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
}
