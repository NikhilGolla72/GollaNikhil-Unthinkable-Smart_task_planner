import React from "react";
import { motion } from "framer-motion";

export default function ModeSelector({ mode, onChange }) {
  const modes = [
    {
      value: "balanced",
      label: "Balanced",
      description: "Realistic timeline with moderate risk",
      icon: "⚖️",
      color: "blue"
    },
    {
      value: "aggressive",
      label: "Aggressive",
      description: "Fast-paced with higher risk",
      icon: "⚡",
      color: "orange"
    },
    {
      value: "safe",
      label: "Safe",
      description: "Conservative approach with lower risk",
      icon: "🛡️",
      color: "green"
    }
  ];

  const getColorClasses = (color, isSelected) => {
    const colorMap = {
      blue: {
        bg: isSelected ? "bg-blue-500" : "bg-blue-100",
        border: isSelected ? "border-blue-500" : "border-blue-200",
        text: isSelected ? "text-white" : "text-blue-700",
        hover: "hover:bg-blue-200"
      },
      orange: {
        bg: isSelected ? "bg-orange-500" : "bg-orange-100",
        border: isSelected ? "border-orange-500" : "border-orange-200",
        text: isSelected ? "text-white" : "text-orange-700",
        hover: "hover:bg-orange-200"
      },
      green: {
        bg: isSelected ? "bg-green-500" : "bg-green-100",
        border: isSelected ? "border-green-500" : "border-green-200",
        text: isSelected ? "text-white" : "text-green-700",
        hover: "hover:bg-green-200"
      }
    };
    return colorMap[color];
  };

  return (
    <div>
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Select Planning Mode</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {modes.map((modeOption) => {
          const isSelected = mode === modeOption.value;
          const colors = getColorClasses(modeOption.color, isSelected);
          
          return (
            <motion.button
              key={modeOption.value}
              onClick={() => onChange(modeOption.value)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className={`p-4 rounded-lg border-2 transition-all duration-200 ${colors.bg} ${colors.border} ${colors.text} ${!isSelected ? colors.hover : ''} cursor-pointer`}
            >
              <div className="text-center">
                <div className="text-2xl mb-2">{modeOption.icon}</div>
                <div className="font-semibold mb-1">{modeOption.label}</div>
                <div className="text-xs opacity-80">{modeOption.description}</div>
              </div>
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}
