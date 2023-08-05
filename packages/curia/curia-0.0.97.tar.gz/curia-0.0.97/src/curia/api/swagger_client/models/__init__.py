# coding: utf-8

# flake8: noqa
"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 1.25.0-develop.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import models into model package
from curia.api.swagger_client.models.aggregation_type import AggregationType
from curia.api.swagger_client.models.analysis import Analysis
from curia.api.swagger_client.models.analysis_job import AnalysisJob
from curia.api.swagger_client.models.analysis_job_config import AnalysisJobConfig
from curia.api.swagger_client.models.analysis_job_output import AnalysisJobOutput
from curia.api.swagger_client.models.analysis_job_status import AnalysisJobStatus
from curia.api.swagger_client.models.analysis_job_type import AnalysisJobType
from curia.api.swagger_client.models.analysis_type import AnalysisType
from curia.api.swagger_client.models.any_of_arithmetic_expression_value import AnyOfArithmeticExpressionValue
from curia.api.swagger_client.models.any_of_boolean_expression_value import AnyOfBooleanExpressionValue
from curia.api.swagger_client.models.any_of_cohort_definition_patient_metadata_filters_items import AnyOfCohortDefinitionPatientMetadataFiltersItems
from curia.api.swagger_client.models.any_of_condition_value import AnyOfConditionValue
from curia.api.swagger_client.models.arithmetic_expression import ArithmeticExpression
from curia.api.swagger_client.models.arithmetic_operator import ArithmeticOperator
from curia.api.swagger_client.models.body import Body
from curia.api.swagger_client.models.body1 import Body1
from curia.api.swagger_client.models.boolean_expression import BooleanExpression
from curia.api.swagger_client.models.code import Code
from curia.api.swagger_client.models.cohort import Cohort
from curia.api.swagger_client.models.cohort_definition import CohortDefinition
from curia.api.swagger_client.models.cohort_filter import CohortFilter
from curia.api.swagger_client.models.cohort_filter_condition import CohortFilterCondition
from curia.api.swagger_client.models.cohort_results import CohortResults
from curia.api.swagger_client.models.cohort_window import CohortWindow
from curia.api.swagger_client.models.condition import Condition
from curia.api.swagger_client.models.condition_operator import ConditionOperator
from curia.api.swagger_client.models.create_many_analysis_dto import CreateManyAnalysisDto
from curia.api.swagger_client.models.create_many_analysis_job_dto import CreateManyAnalysisJobDto
from curia.api.swagger_client.models.create_many_analysis_job_output_dto import CreateManyAnalysisJobOutputDto
from curia.api.swagger_client.models.create_many_analysis_job_status_dto import CreateManyAnalysisJobStatusDto
from curia.api.swagger_client.models.create_many_code_dto import CreateManyCodeDto
from curia.api.swagger_client.models.create_many_cohort_dto import CreateManyCohortDto
from curia.api.swagger_client.models.create_many_data_query_dto import CreateManyDataQueryDto
from curia.api.swagger_client.models.create_many_dataset_column_dto import CreateManyDatasetColumnDto
from curia.api.swagger_client.models.create_many_dataset_dto import CreateManyDatasetDto
from curia.api.swagger_client.models.create_many_dataset_job_dto import CreateManyDatasetJobDto
from curia.api.swagger_client.models.create_many_feature_category_dto import CreateManyFeatureCategoryDto
from curia.api.swagger_client.models.create_many_feature_dto import CreateManyFeatureDto
from curia.api.swagger_client.models.create_many_feature_sub_category_dto import CreateManyFeatureSubCategoryDto
from curia.api.swagger_client.models.create_many_model_batch_dto import CreateManyModelBatchDto
from curia.api.swagger_client.models.create_many_model_batch_job_dto import CreateManyModelBatchJobDto
from curia.api.swagger_client.models.create_many_model_dataset_dto import CreateManyModelDatasetDto
from curia.api.swagger_client.models.create_many_model_dto import CreateManyModelDto
from curia.api.swagger_client.models.create_many_model_job_dto import CreateManyModelJobDto
from curia.api.swagger_client.models.create_many_model_job_output_dto import CreateManyModelJobOutputDto
from curia.api.swagger_client.models.create_many_model_job_output_feature_dto import CreateManyModelJobOutputFeatureDto
from curia.api.swagger_client.models.create_many_model_population_dto import CreateManyModelPopulationDto
from curia.api.swagger_client.models.create_many_organization_dto import CreateManyOrganizationDto
from curia.api.swagger_client.models.create_many_organization_feature_exclusion_dto import CreateManyOrganizationFeatureExclusionDto
from curia.api.swagger_client.models.create_many_organization_setting_dto import CreateManyOrganizationSettingDto
from curia.api.swagger_client.models.create_many_process_dto import CreateManyProcessDto
from curia.api.swagger_client.models.create_many_process_job_dto import CreateManyProcessJobDto
from curia.api.swagger_client.models.create_many_process_job_output_dto import CreateManyProcessJobOutputDto
from curia.api.swagger_client.models.create_many_process_job_status_dto import CreateManyProcessJobStatusDto
from curia.api.swagger_client.models.create_many_project_dto import CreateManyProjectDto
from curia.api.swagger_client.models.create_many_project_member_dto import CreateManyProjectMemberDto
from curia.api.swagger_client.models.create_many_user_favorite_dto import CreateManyUserFavoriteDto
from curia.api.swagger_client.models.data_query import DataQuery
from curia.api.swagger_client.models.data_table import DataTable
from curia.api.swagger_client.models.database import Database
from curia.api.swagger_client.models.dataset import Dataset
from curia.api.swagger_client.models.dataset_column import DatasetColumn
from curia.api.swagger_client.models.dataset_job import DatasetJob
from curia.api.swagger_client.models.dataset_job_status import DatasetJobStatus
from curia.api.swagger_client.models.feature import Feature
from curia.api.swagger_client.models.feature_category import FeatureCategory
from curia.api.swagger_client.models.feature_sub_category import FeatureSubCategory
from curia.api.swagger_client.models.feature_table import FeatureTable
from curia.api.swagger_client.models.geographic_counts import GeographicCounts
from curia.api.swagger_client.models.geographic_queries import GeographicQueries
from curia.api.swagger_client.models.get_many_analysis_job_output_response_dto import GetManyAnalysisJobOutputResponseDto
from curia.api.swagger_client.models.get_many_analysis_job_response_dto import GetManyAnalysisJobResponseDto
from curia.api.swagger_client.models.get_many_analysis_job_status_response_dto import GetManyAnalysisJobStatusResponseDto
from curia.api.swagger_client.models.get_many_analysis_response_dto import GetManyAnalysisResponseDto
from curia.api.swagger_client.models.get_many_code_response_dto import GetManyCodeResponseDto
from curia.api.swagger_client.models.get_many_cohort_response_dto import GetManyCohortResponseDto
from curia.api.swagger_client.models.get_many_data_query_response_dto import GetManyDataQueryResponseDto
from curia.api.swagger_client.models.get_many_data_table_response_dto import GetManyDataTableResponseDto
from curia.api.swagger_client.models.get_many_database_response_dto import GetManyDatabaseResponseDto
from curia.api.swagger_client.models.get_many_dataset_column_response_dto import GetManyDatasetColumnResponseDto
from curia.api.swagger_client.models.get_many_dataset_job_response_dto import GetManyDatasetJobResponseDto
from curia.api.swagger_client.models.get_many_dataset_job_status_response_dto import GetManyDatasetJobStatusResponseDto
from curia.api.swagger_client.models.get_many_dataset_response_dto import GetManyDatasetResponseDto
from curia.api.swagger_client.models.get_many_feature_category_response_dto import GetManyFeatureCategoryResponseDto
from curia.api.swagger_client.models.get_many_feature_response_dto import GetManyFeatureResponseDto
from curia.api.swagger_client.models.get_many_feature_sub_category_response_dto import GetManyFeatureSubCategoryResponseDto
from curia.api.swagger_client.models.get_many_model_batch_job_response_dto import GetManyModelBatchJobResponseDto
from curia.api.swagger_client.models.get_many_model_batch_response_dto import GetManyModelBatchResponseDto
from curia.api.swagger_client.models.get_many_model_dataset_response_dto import GetManyModelDatasetResponseDto
from curia.api.swagger_client.models.get_many_model_job_output_feature_response_dto import GetManyModelJobOutputFeatureResponseDto
from curia.api.swagger_client.models.get_many_model_job_output_response_dto import GetManyModelJobOutputResponseDto
from curia.api.swagger_client.models.get_many_model_job_response_dto import GetManyModelJobResponseDto
from curia.api.swagger_client.models.get_many_model_job_status_response_dto import GetManyModelJobStatusResponseDto
from curia.api.swagger_client.models.get_many_model_population_response_dto import GetManyModelPopulationResponseDto
from curia.api.swagger_client.models.get_many_model_response_dto import GetManyModelResponseDto
from curia.api.swagger_client.models.get_many_organization_feature_exclusion_response_dto import GetManyOrganizationFeatureExclusionResponseDto
from curia.api.swagger_client.models.get_many_organization_response_dto import GetManyOrganizationResponseDto
from curia.api.swagger_client.models.get_many_organization_setting_response_dto import GetManyOrganizationSettingResponseDto
from curia.api.swagger_client.models.get_many_process_job_output_response_dto import GetManyProcessJobOutputResponseDto
from curia.api.swagger_client.models.get_many_process_job_response_dto import GetManyProcessJobResponseDto
from curia.api.swagger_client.models.get_many_process_job_status_response_dto import GetManyProcessJobStatusResponseDto
from curia.api.swagger_client.models.get_many_process_response_dto import GetManyProcessResponseDto
from curia.api.swagger_client.models.get_many_project_member_response_dto import GetManyProjectMemberResponseDto
from curia.api.swagger_client.models.get_many_project_response_dto import GetManyProjectResponseDto
from curia.api.swagger_client.models.get_many_user_favorite_response_dto import GetManyUserFavoriteResponseDto
from curia.api.swagger_client.models.intervention_definition import InterventionDefinition
from curia.api.swagger_client.models.json import Json
from curia.api.swagger_client.models.logical_operator import LogicalOperator
from curia.api.swagger_client.models.model import Model
from curia.api.swagger_client.models.model_batch import ModelBatch
from curia.api.swagger_client.models.model_batch_job import ModelBatchJob
from curia.api.swagger_client.models.model_dataset import ModelDataset
from curia.api.swagger_client.models.model_job import ModelJob
from curia.api.swagger_client.models.model_job_config import ModelJobConfig
from curia.api.swagger_client.models.model_job_event import ModelJobEvent
from curia.api.swagger_client.models.model_job_output import ModelJobOutput
from curia.api.swagger_client.models.model_job_output_feature import ModelJobOutputFeature
from curia.api.swagger_client.models.model_job_status import ModelJobStatus
from curia.api.swagger_client.models.model_population import ModelPopulation
from curia.api.swagger_client.models.organization import Organization
from curia.api.swagger_client.models.organization_feature_exclusion import OrganizationFeatureExclusion
from curia.api.swagger_client.models.organization_setting import OrganizationSetting
from curia.api.swagger_client.models.outcome_definition import OutcomeDefinition
from curia.api.swagger_client.models.period_definition import PeriodDefinition
from curia.api.swagger_client.models.period_type import PeriodType
from curia.api.swagger_client.models.person_set import PersonSet
from curia.api.swagger_client.models.process import Process
from curia.api.swagger_client.models.process_job import ProcessJob
from curia.api.swagger_client.models.process_job_output import ProcessJobOutput
from curia.api.swagger_client.models.process_job_status import ProcessJobStatus
from curia.api.swagger_client.models.process_type import ProcessType
from curia.api.swagger_client.models.project import Project
from curia.api.swagger_client.models.project_member import ProjectMember
from curia.api.swagger_client.models.select_expression import SelectExpression
from curia.api.swagger_client.models.set_operator import SetOperator
from curia.api.swagger_client.models.update_user_dto import UpdateUserDto
from curia.api.swagger_client.models.user_favorite import UserFavorite
