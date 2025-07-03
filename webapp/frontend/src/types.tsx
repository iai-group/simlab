export type Resource = {
  id: string;
  name: string;
  description: string;
  arguments: Array<Argument>;
};

export type Argument = {
  name: string;
  type: string;
  value: any;
};

export type Task = Resource & {
  metrics: Array<Metric>;
};

export type Metric = Resource;

export type Agent = Resource;

export type Simulator = Resource;

export type System = {
  id: string;
  type: string;
  image: string;
  arguments: Array<Object>;
  parameters: Object;
  class_name: string;
};
