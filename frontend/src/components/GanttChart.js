import React from "react";
import { motion } from "framer-motion";

export default function GanttChart({ tasks, criticalPath = [] }) {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        No tasks to display
      </div>
    );
  }

  // Calculate the date range
  const dates = tasks.flatMap(task => [task.start, task.end]).filter(Boolean);
  const minDate = new Date(Math.min(...dates.map(d => new Date(d))));
  const maxDate = new Date(Math.max(...dates.map(d => new Date(d))));
  
  // Add some padding
  minDate.setDate(minDate.getDate() - 1);
  maxDate.setDate(maxDate.getDate() + 1);

  const totalDays = Math.ceil((maxDate - minDate) / (1000 * 60 * 60 * 24));
  const dayWidth = Math.max(60, Math.min(120, 800 / totalDays)); // Responsive width

  const getTaskPosition = (task, index) => {
    const startDate = new Date(task.start);
    const endDate = new Date(task.end);
    
    const startOffset = Math.ceil((startDate - minDate) / (1000 * 60 * 60 * 24));
    const duration = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
    
    // Group tasks by team member for parallel display
    const teamMember = task.team_member || "1";
    const baseRowHeight = 60;
    const teamMemberOffset = (parseInt(teamMember) - 1) * 15; // Offset for team members
    
    return {
      left: startOffset * dayWidth,
      width: Math.max(duration * dayWidth, 40), // Minimum width for visibility
      top: index * baseRowHeight + teamMemberOffset
    };
  };

  const getRiskColor = (riskScore, isCritical) => {
    if (isCritical) {
      if (riskScore >= 4) return "bg-red-500";
      if (riskScore >= 3) return "bg-orange-500";
      return "bg-yellow-500";
    } else {
      if (riskScore >= 4) return "bg-red-300";
      if (riskScore >= 3) return "bg-yellow-300";
      return "bg-green-300";
    }
  };

  // Generate date labels
  const dateLabels = [];
  for (let i = 0; i <= totalDays; i += Math.max(1, Math.floor(totalDays / 10))) {
    const date = new Date(minDate);
    date.setDate(date.getDate() + i);
    dateLabels.push({
      date: date.toLocaleDateString(),
      offset: i * dayWidth
    });
  }

  return (
    <div className="overflow-x-auto">
      <div className="min-w-full">
        {/* Date Header */}
        <div className="relative h-12 bg-gray-50 border-b border-gray-200 mb-4">
          <div className="absolute inset-0" style={{ width: `${totalDays * dayWidth}px` }}>
            {dateLabels.map((label, index) => (
              <div
                key={index}
                className="absolute top-0 h-full flex items-center text-xs text-gray-600 border-r border-gray-200 px-2"
                style={{ left: `${label.offset}px`, width: `${dayWidth}px` }}
              >
                {label.date}
              </div>
            ))}
          </div>
        </div>

        {/* Tasks */}
        <div className="relative" style={{ width: `${totalDays * dayWidth}px` }}>
          {tasks.map((task, index) => {
            const position = getTaskPosition(task, index);
            const isCritical = criticalPath.includes(task.id);
            
            return (
              <motion.div
                key={task.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="mb-3 flex items-center relative"
                style={{ top: position.top }}
              >
                {/* Task Label */}
                <div className="w-48 pr-4 flex-shrink-0">
                  <div className="text-sm font-medium text-gray-800 truncate">
                    {task.title}
                  </div>
                  <div className="text-xs text-gray-500">
                    {task.est_hours}h • Risk: {task.risk_score}/5
                    {task.team_member && (
                      <span className="ml-2 text-blue-600 font-semibold">
                        • Member {task.team_member}
                      </span>
                    )}
                  </div>
                </div>

                {/* Task Bar */}
                <div className="relative flex-1 h-8 bg-gray-100 rounded">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${position.width}px` }}
                    transition={{ duration: 0.6, delay: index * 0.1 + 0.2 }}
                    className={`absolute top-0 h-full rounded ${getRiskColor(task.risk_score, isCritical)} ${
                      isCritical ? 'ring-2 ring-red-400 ring-opacity-50' : ''
                    }`}
                    style={{ left: `${position.left}px` }}
                  >
                    <div className="h-full flex items-center justify-center">
                      <span className="text-white text-xs font-semibold px-2 truncate">
                        {task.est_hours}h
                      </span>
                    </div>
                  </motion.div>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Legend */}
        <div className="mt-6 flex flex-wrap gap-4 text-sm">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-green-300 rounded mr-2"></div>
            <span>Low Risk</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-yellow-300 rounded mr-2"></div>
            <span>Medium Risk</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-red-300 rounded mr-2"></div>
            <span>High Risk</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-red-500 rounded mr-2 ring-2 ring-red-400 ring-opacity-50"></div>
            <span>Critical Path</span>
          </div>
        </div>
      </div>
    </div>
  );
}
