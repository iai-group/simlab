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
  type: string;
  id: string;
  image: string;
  parameters: Object;
};
