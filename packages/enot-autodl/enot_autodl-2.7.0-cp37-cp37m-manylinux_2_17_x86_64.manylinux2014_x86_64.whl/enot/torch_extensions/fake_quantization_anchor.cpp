#include <torch/script.h>
#include <torch/extension.h>

torch::Tensor fake_quantization_anchor(torch::Tensor X, torch::Tensor threshold)
{
    return X.clone();
}

static auto registry = torch::RegisterOperators("enot::fake_quantization_anchor", &fake_quantization_anchor);

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m)
{
    m.def("fake_quantization_anchor", &fake_quantization_anchor, "Fake quantization anchor");
}
