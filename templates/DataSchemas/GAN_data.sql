CREATE TABLE "discriminator_jobs" (
  "id" int PRIMARY KEY,
  "version" SERIAL,
  "date_time_start" datetime DEFAULT (now()),
  "date_time_stop" datetime,
  "sound_type" int,
  "train_accuracy" double,
  "test_accuracy" double,
  "hyperparameters" int,
  "model_location" varchar
);

CREATE TABLE "discriminator_hyperparameters" (
  "id" int PRIMARY KEY,
  "learning_rate" double,
  "sampling_rate" int,
  "epochs" int,
  "k_folds" int,
  "number_mfcc" int,
  "batch_size" int,
  "buffer_size" int,
  "loss" double
);

CREATE TABLE "sound_type" (
  "id" int PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "generator_jobs" (
  "id" int PRIMARY KEY,
  "version" int,
  "date_time_start" datetime DEFAULT (now()),
  "date_time_stop" datetime,
  "model_location" varchar,
  "hyperparameters" int
);

CREATE TABLE "generator_hyperparameters" (
  "id" int PRIMARY KEY,
  "max_number_generate" int,
  "batch_size" int,
  "noise_dim" int,
  "loss" double
);

ALTER TABLE "discriminator_jobs" ADD FOREIGN KEY ("sound_type") REFERENCES "sound_type" ("id");

ALTER TABLE "discriminator_jobs" ADD FOREIGN KEY ("hyperparameters") REFERENCES "discriminator_hyperparameters" ("id");

ALTER TABLE "generator_jobs" ADD FOREIGN KEY ("hyperparameters") REFERENCES "generator_hyperparameters" ("id");
