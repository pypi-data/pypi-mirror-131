import numpy as np
import pytest
from qcalibrateremote.builders import (
    ConfigurationBuilder,
    InvalidConfigurationException,
    ParameterBuilder,
    PulseBuilder,
)


@pytest.fixture
def configuration_builder():
    return ConfigurationBuilder(ConfigurationBuilder._create_cfg_parameter("name"))


@pytest.fixture
def pulse_builder():
    cfg = {
        "pulse_name": "pulse1",
        "upper_limit": 15.0,
        "lower_limit": -15.0,
        "bins_number": 11,
        "time_name": "time1",
        "amplitude_variation": 0.5,
        "basis": {
            "basis_name": "Fourier",
            "basis_class": "Fourier",
            "basis_module": "quocslib.pulses.basis.Fourier",
            "basis_vector_number": 10,
            "random_super_parameter_distribution": {
                "distribution_name": "Uniform",
                "distribution_class": "Uniform",
                "distribution_module": "quocslib.pulses.super_parameter.Uniform",
                "lower_limit": 0.1,
                "upper_limit": 30.0,
            },
        },
        "scaling_function": {
            "function_type": "lambda_function",
            "lambda_function": "lambda t: 1.0 + 0.0*t",
        },
        "initial_guess": {
            "function_type": "lambda_function",
            "lambda_function": "lambda t: np.pi/3 + 0.0*t",
        },
    }

    return PulseBuilder(cfg)


@pytest.fixture
def parameter_builder():
    return ParameterBuilder(ParameterBuilder._create_cfg("test"))


def test_PulseBuilder_invalid_scaling_function_throws(pulse_builder: PulseBuilder):

    with pytest.raises(InvalidConfigurationException) as e_info:
        with pulse_builder.scaling_function() as scaling_function:
            scaling_function.function = "yxjui"

    assert "yxjui" in e_info.value.args[0]


def test_PulseBuilder_scaling_function_lambda(pulse_builder: PulseBuilder):
    with pulse_builder.scaling_function() as scaling_function:
        scaling_function.function = "lambda t: 1.0"

    with pulse_builder.scaling_function() as scaling_function:
        assert scaling_function.type == "lambda_function"
        assert scaling_function.function == "lambda t: 1.0"


def test_PulseBuilder_scaling_function_lambda_numpy(pulse_builder: PulseBuilder):
    with pulse_builder.scaling_function() as scaling_function:
        scaling_function.function = "lambda t: np.pi"

    with pulse_builder.scaling_function() as scaling_function:
        assert scaling_function.type == "lambda_function"
        assert scaling_function.function == "lambda t: np.pi"


def test_PulseBuilder_scaling_function_lambda_scipy_throws(pulse_builder: PulseBuilder):
    with pytest.raises(InvalidConfigurationException):
        with pulse_builder.scaling_function() as scaling_function:
            scaling_function.function = "lambda t: scipy.pi"


def test_PulseBuilder_scaling_function_two_arguments_lambda_throws(
    pulse_builder: PulseBuilder,
):
    with pytest.raises(InvalidConfigurationException):
        with pulse_builder.scaling_function() as scaling_function:
            scaling_function.function = "lambda x,y: x*y"


def test_PulseBuilder_scaling_function_values(pulse_builder: PulseBuilder):
    with pulse_builder.scaling_function() as scaling_function:
        scaling_function.function = [0, 1.2, 2, 1.2, 0]

    with pulse_builder.scaling_function() as scaling_function:
        assert scaling_function.type == "list_function"
        assert scaling_function.function == [0, 1.2, 2, 1.2, 0]
        assert scaling_function._cfg[scaling_function.type] == [0.0, 1.2, 2.0, 1.2, 0.0]


def test_PulseBuilder_scaling_function_numpy_array(pulse_builder: PulseBuilder):
    with pulse_builder.scaling_function() as scaling_function:
        scaling_function.function = 4 - (np.linspace(0, 4, 5) - 2) ** 2

    with pulse_builder.scaling_function() as scaling_function:
        assert scaling_function.type == "list_function"
        assert scaling_function.function == [0, 3, 4, 3, 0]
        assert scaling_function._cfg[scaling_function.type] == [0, 3, 4, 3, 0]


def test_PulseBuilder_scaling_function_matrix_throws(pulse_builder: PulseBuilder):
    with pytest.raises(InvalidConfigurationException):
        with pulse_builder.scaling_function() as scaling_function:
            scaling_function.function = [[0, 1.2], [2, 1.2]]


def test_PulseBuilder_scaling_function_ndarray(pulse_builder: PulseBuilder):
    with pulse_builder.scaling_function() as scaling_function:
        scaling_function.function = np.asarray([0, 1, 2, 1, 0])

    with pulse_builder.scaling_function() as scaling_function:
        assert scaling_function.type == "list_function"
        assert scaling_function.function == [0, 1, 2, 1, 0]
        assert scaling_function._cfg[scaling_function.type] == [0, 1, 2, 1, 0]


def test_ConfigurationBuilder_AddParameter(configuration_builder):
    with configuration_builder.parameter("P1") as p1:
        p1.lower_limit = -0.1
        p1.initial_value = 0.1
        p1.upper_limit = 0.7
        p1.initial_variation = 0.05

    with configuration_builder.parameter("P1") as p1:
        assert p1.name == "P1"
        assert p1.lower_limit == -0.1
        assert p1.initial_value == 0.1
        assert p1.upper_limit == 0.7
        assert p1.initial_variation == 0.05


def test_ConfigurationBuilder_Add2Parameters(configuration_builder):
    with configuration_builder.parameter("P1") as p1:
        p1.lower_limit = -0.1
        p1.initial_value = 0.1
        p1.upper_limit = 0.7
        p1.initial_variation = 0.05

    with configuration_builder.parameter("P2") as p2:
        p2.lower_limit = -0.1
        p2.initial_value = 0.1
        p2.upper_limit = 0.7
        p2.initial_variation = 0.05

    with configuration_builder.parameter("P1") as p1:
        assert p1.name == "P1"
        assert p1.lower_limit == -0.1
        assert p1.initial_value == 0.1
        assert p1.upper_limit == 0.7
        assert p1.initial_variation == 0.05

    with configuration_builder.parameter("P2") as p2:
        assert p2.name == "P2"
        assert p2.lower_limit == -0.1
        assert p2.initial_value == 0.1
        assert p2.upper_limit == 0.7
        assert p2.initial_variation == 0.05


def test_ConfigurationBuilder_IQpulse_works():
    configuration = ConfigurationBuilder(ConfigurationBuilder._create_cfg_dcrab("name"))

    with configuration.time("time1") as time1:
        time1.initial_value = 32
        time1.optimize = False

    with configuration.pulse("pulse_I") as pulse_I:
        pulse_I.time_name = "time1"
        pulse_I.lower_limit = 0
        pulse_I.upper_limit = 1
        pulse_I.variation = 0.015
        pulse_I.bins_number = 33

        with pulse_I.initial_guess() as initial_guess:
            initial_guess.function = "lambda t: %f" % (0.64)
        with pulse_I.scaling_function() as scaling_function:
            scaling_function.function = "lambda t: np.exp(-(t - 16)**2/(2*8**2))"
        with pulse_I.fourier_basis() as fourier_basis:
            fourier_basis.basis_vector_number = 3
            with fourier_basis.uniform_super_parameter_distribution() as uniform_super_parameter_distribution:
                uniform_super_parameter_distribution.lower_limit = 0.1
                uniform_super_parameter_distribution.upper_limit = 5

    with configuration.pulse("pulse_Q") as pulse_Q:
        pulse_Q.time_name = "time1"
        assert pulse_Q.time_name == "time1"
        pulse_Q.lower_limit = -1
        assert pulse_Q.lower_limit == -1
        pulse_Q.upper_limit = 1
        assert pulse_Q.upper_limit == 1
        pulse_Q.variation = 0.015
        assert pulse_Q.variation == 0.015
        pulse_Q.bins_number = 33
        assert pulse_Q.bins_number == 33
        with pulse_Q.initial_guess() as initial_guess:
            initial_guess.function = "lambda t: %f" % (0.01)
        with pulse_Q.scaling_function() as scaling_function:
            scaling_function.function = (
                "lambda t: -(t -16)/8 * np.exp(0.5) * np.exp(-(t - 16)**2/(2*8**2))"
            )
        with pulse_Q.fourier_basis() as fourier_basis:
            fourier_basis.basis_vector_number = 3
            assert fourier_basis.basis_vector_number == 3
            with fourier_basis.uniform_super_parameter_distribution() as uniform_super_parameter_distribution:
                uniform_super_parameter_distribution.lower_limit = 0.1
                uniform_super_parameter_distribution.upper_limit = 5

    with configuration.dcrab_settings() as dcrab_settings:
        dcrab_settings.maximum_iterations_per_super_iteration = 5
        dcrab_settings.super_iteration_number = 2

    assert configuration._cfg == {
        "optimization_dictionary": {
            "optimization_client_name": "name",
            "opti_algorithm_name": "dCRAB",
            "opti_algorithm_module": "quocslib.optimalalgorithms.dCRABAlgorithm",
            "opti_algorithm_class": "DCrabAlgorithm",
            "algorithm_settings": {
                "super_iteration_number": 2,
                "maximum_function_evaluations_number": 5,
            },
            "dsm_settings": {
                "general_settings": {"dsm_name": "nelder_mead", "is_adaptive": True},
                "stopping_criteria": {
                    "iterations_number": 100,
                    "xatol": 1e-13,
                    "frtol": 1e-13,
                },
            },
            "pulses": [
                {
                    "pulse_name": "pulse_I",
                    "upper_limit": 1.0,
                    "lower_limit": 0.0,
                    "bins_number": 33,
                    "time_name": "time1",
                    "amplitude_variation": 0.5,
                    "basis": {
                        "basis_name": "Fourier",
                        "basis_class": "Fourier",
                        "basis_module": "quocslib.pulses.basis.Fourier",
                        "basis_vector_number": 3,
                        "random_super_parameter_distribution": {
                            "distribution_name": "Uniform",
                            "distribution_class": "Uniform",
                            "distribution_module": "quocslib.pulses.super_parameter.Uniform",
                            "lower_limit": 0.1,
                            "upper_limit": 5.0,
                        },
                    },
                    "scaling_function": {
                        "function_type": "lambda_function",
                        "lambda_function": "lambda t: np.exp(-(t - 16)**2/(2*8**2))",
                    },
                    "initial_guess": {
                        "function_type": "lambda_function",
                        "lambda_function": "lambda t: 0.640000",
                    },
                },
                {
                    "pulse_name": "pulse_Q",
                    "upper_limit": 1.0,
                    "lower_limit": -1.0,
                    "bins_number": 33,
                    "time_name": "time1",
                    "amplitude_variation": 0.5,
                    "basis": {
                        "basis_name": "Fourier",
                        "basis_class": "Fourier",
                        "basis_module": "quocslib.pulses.basis.Fourier",
                        "basis_vector_number": 3,
                        "random_super_parameter_distribution": {
                            "distribution_name": "Uniform",
                            "distribution_class": "Uniform",
                            "distribution_module": "quocslib.pulses.super_parameter.Uniform",
                            "lower_limit": 0.1,
                            "upper_limit": 5.0,
                        },
                    },
                    "scaling_function": {
                        "function_type": "lambda_function",
                        "lambda_function": "lambda t: -(t -16)/8 * np.exp(0.5) * np.exp(-(t - 16)**2/(2*8**2))",
                    },
                    "initial_guess": {
                        "function_type": "lambda_function",
                        "lambda_function": "lambda t: 0.010000",
                    },
                },
            ],
            "times": [
                {"time_name": "time1", "initial_value": 32, "is_optimization": False}
            ],
            "parameters": [],
        },
        "communication": {"communication_type": "AllInOneCommunication"},
        "figure_of_merit": {"further_args": [], "program_type": "ClientDefined"},
    }


def test_ConfigurationBuilder_parameter_with_name_duplicate_throws():
    builder = ConfigurationBuilder(ConfigurationBuilder._create_cfg_parameter("name"))
    with builder.parameter("P1") as p1:
        p1.lower_limit = -0.1
        p1.initial_value = 0.1
        p1.upper_limit = 0.7
        p1.initial_variation = 0.05

    # duplicate a parameter
    builder._parameters.append(builder._parameters[0])

    with pytest.raises(InvalidConfigurationException):
        with builder.parameter("P1") as p1:
            p1.initial_value == 0.0


def test_PulseBuilder_parameter_with_name_duplicate_throws():
    builder = ConfigurationBuilder(ConfigurationBuilder._create_cfg_parameter("name"))
    with builder.parameter("P1") as p1:
        p1.lower_limit = -0.1
        p1.initial_value = 0.1
        p1.upper_limit = 0.7
        p1.initial_variation = 0.05

    # duplicate a parameter
    builder._parameters.append(builder._parameters[0])

    with pytest.raises(InvalidConfigurationException):
        with builder.parameter("P1") as p1:
            p1.initial_value == 0.0


def test_ParameterBuilder_initial_value_higher_than_upper_limit_validate_throws(
    parameter_builder: ParameterBuilder,
):
    parameter_builder.initial_value = parameter_builder.upper_limit + 0.1
    with pytest.raises(InvalidConfigurationException):
        parameter_builder.validate()


def test_ParameterBuilder_initial_value_lower_than_lower_limit_validate_throws(
    parameter_builder: ParameterBuilder,
):
    parameter_builder.initial_value = parameter_builder.lower_limit - 0.1
    with pytest.raises(InvalidConfigurationException):
        parameter_builder.validate()


def test_ParameterBuilder_initial_value_equal_to_lower_and_upper_limits_validate_throws(
    parameter_builder: ParameterBuilder,
):
    parameter_builder.lower_limit = parameter_builder.initial_value
    parameter_builder.upper_limit = parameter_builder.initial_value
    with pytest.raises(InvalidConfigurationException):
        parameter_builder.validate()


def test_ParameterBuilder_variation_bigger_than_range_validate_throws(
    parameter_builder: ParameterBuilder,
):
    parameter_builder.initial_variation = (
        parameter_builder.upper_limit - parameter_builder.lower_limit + 0.1
    )
    with pytest.raises(InvalidConfigurationException):
        parameter_builder.validate()
