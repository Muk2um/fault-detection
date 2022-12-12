from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
import numpy as np 
import sys,os
from sklearn.preprocessing import pipeline 
import pandas as pd 
from typing import Optional
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sensor.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder


class DataTransformation:


    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)

    @classmethod
    def get_data_transformer_object(cls)->pipeline:
        try:
            simple_imputer=SimpleImputer(strategy='constant',fill_value=0)
            robust_scaler=RobustScaler()
            pipeline=pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('RobustScaler',robust_scaler)
               ])   
            return pipeline        

        except Exception as e:
            raise e

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            input_feature_train_df = train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN,axis=1)

            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_test_df=test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            target_feature_train_arr=label_encoder.transform(target_feature_train_df)
            target_feature_test_arr=label_encoder.transform(target_feature_test_df)

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            input_feature_train_arr = transformation_pipeline.fit(input_feature_train_df)
            input_feature_test_arr = tranformation_pipeline.transform(input_feature_test_df)


            smt = SMOTETomek(sampling_strategy="minority")
            logging.info(f"Before resampling in training set input : {input_feature_train_arr.shape} Target : {target_feature_train_arr}")
            input_feature_train_arr,target_feature_train_arr = smt.fit_resample(input_feature_train_arr,target_feature_train_arr)
            logging.info(f"After resampling in training set input : {input_feature_train_arr.shape} Target : {target_feature_train_arr}")

            logging.info(f"Before resampling in testing set input : {input_feature_test_arr.shape} Target : {target_feature_test_arr}")
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr,target_feature_test_arr)
            logging.info(f"After resampling in testing set input : {input_feature_test_arr.shape} Target : {target_feature_test_arr}")


            train_arr = np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_arr]
            


            #save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)


            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
             obj=transformation_pipleine)

            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
            obj=label_encoder)



            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path

            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact






        except Exception as e:
            raise SensorException(e, sys)
       


