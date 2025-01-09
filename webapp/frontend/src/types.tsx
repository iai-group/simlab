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

export type Task = Resource;

export type Metric = Resource;

export type Agent = Resource;

export type Simulator = Resource;
