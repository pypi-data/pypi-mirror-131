# Changelog
Here you will find a changelog of all the SDK releases.

## [5.1.1] 2021-12-14
Added support for infer dtypes

## [5.0.3] 2021-12-14
This release does not have any breaking changes.
This release adds an SDK reference guide to our SDK.

## [5.0.1] 2021-12-01
This release has breaking changes - change schema creation mechanism
- Drop support for data_entity.generate_summary() and replace with improved data_entity.summarise()
- Drop support for upload models using baseline_files list of files
- Improved feature importance feature: new parameters in summarize():
  - importance_sample - a float value, used to sample the data while calculate the Feature importance
  - importance_target_label - an option to pass a label field name
- Remove deprecated task as a param to EntitiesValidator

## [4.2.3] 2021-12-07
- fix bug in binning for numeric features with null values

## [4.2.2] 2021-12-01
- Change the binning mechanism for numeric data entities

## [4.1.0] 2021-11-28
This release has breaking changes - add functionality for transaction:
- add functionality to upload data from s3 to superwise
- add functionality to upload data from gcs to superwise

## [4.0.0] 2021-11-23
This release has breaking changes - task changed following properties:
- task_description &rarr; description
- title &rarr; name
- task_type &rarr; removed

## [3.2.0] - 2021-11-16
This release has breaking changes.
Refactor tasks model

## [3.1.2] - 2021-11-15

Improve requirements.txt - lock versions and added jwt as a requirement.

remove DEBUG mode

log.debug added for each API call

## [3.1.0] - 2021-11-11
This release has breaking changes.
removed client_name as a param from superwise object


## [3.0.0] - 2021-10-19
This release has breaking changes.
We define new entity named transaction, which responsible to manage all the data send to superwise.

### Added
- Add Class Transaction, which have 2 methods to send data to superwise (file , batch).

### Removed
- Removed Data Class and send_file methods, for send data to superwise you should use the Transaction class.
