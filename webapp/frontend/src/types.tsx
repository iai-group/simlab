export type Resource = {
  id: string;
  name: string;
  description: string;
};

export type Argument = {
  name: string;
  type: string;
};

export type Task = Resource & {
  arguments: Array<Argument>;
};

export type Metric = Resource & {
  arguments: Array<Argument>;
};

export type Agent = Resource;

export type Simulator = Resource;
