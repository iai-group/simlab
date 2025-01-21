// Component to display the description of a task

import { Collapse, Container } from "react-bootstrap";
import { Metric, Task } from "../../types";
import React, { useState } from "react";

const TaskDescription: React.FC<{ task: Task }> = ({ task }) => {
  const [visibleMetricIndex, setVisibleMetricIndex] = useState<number | null>(
    null
  );

  const toggleMetricDetails = (index: number) => {
    setVisibleMetricIndex(visibleMetricIndex === index ? null : index);
  };

  const renderArgumentDetails = (argument: any, level: number = 0) => {
    if (typeof argument === "object" && !Array.isArray(argument)) {
      return (
        <div style={{ paddingLeft: `${level * 20}px` }}>
          {Object.entries(argument).map(([key, value], idx) => (
            <div key={`${key}-${idx}`}>
              <strong>{key}:</strong>{" "}
              {typeof value === "object" ? (
                renderArgumentDetails(value, level + 1)
              ) : (
                <span>{String(value)}</span>
              )}
            </div>
          ))}
        </div>
      );
    } else if (Array.isArray(argument)) {
      return (
        <ul style={{ paddingLeft: `${level * 20}px` }}>
          {argument.map((item, idx) => (
            <li key={idx}>{renderArgumentDetails(item, level + 1)}</li>
          ))}
        </ul>
      );
    } else {
      return <span>{String(argument)}</span>;
    }
  };

  const renderMetrics = (metrics: Metric[]) => {
    return metrics.map((metric, index) => {
      const isExpanded = visibleMetricIndex === index;

      return (
        <div key={index} className="metric">
          <div
            style={{ display: "flex", alignItems: "center", cursor: "pointer" }}
            onClick={() => toggleMetricDetails(index)}
            aria-controls={`metric-details-${index}`}
            aria-expanded={isExpanded}
          >
            <span style={{ marginRight: "8px", transition: "transform 0.2s" }}>
              {isExpanded ? "▼" : "▶"}
            </span>
            <h6 style={{ margin: 0 }}>{metric.name}</h6>
          </div>
          {metric.description && <p>{metric.description}</p>}
          <Collapse in={isExpanded}>
            <div id={`metric-details-${index}`} style={{ marginLeft: "20px" }}>
              <i>Arguments</i>
              {metric.arguments && metric.arguments.length > 0 ? (
                metric.arguments.map((arg, idx) => (
                  <div key={idx} className="metric-argument">
                    <strong>{arg.name}:</strong>{" "}
                    {renderArgumentDetails(arg.value)}
                  </div>
                ))
              ) : (
                <p>No arguments available for this metric.</p>
              )}
            </div>
          </Collapse>
        </div>
      );
    });
  };
  return (
    <Container>
      <h1>{task.name}</h1>
      <p>{task.description}</p>
      <div className="metrics">
        <h3>Metrics</h3>
        {task.metrics && task.metrics.length > 0 ? (
          renderMetrics(task.metrics)
        ) : (
          <p>No metrics available.</p>
        )}
      </div>
    </Container>
  );
};

export default TaskDescription;
