"use client"

import type React from "react"
import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  ArrowLeft,
  Activity,
  Calculator,
  TrendingUp,
  Sparkles,
  Heart,
  AlertTriangle,
  CheckCircle,
  Info,
  Apple,
  Utensils,
  Star,
  Leaf,
  Wheat,
  Beef,
  Shield,
  Target,
} from "lucide-react"

// Enhanced interface to match backend response
interface FoodRecommendation {
  name: string
  category: string
  calories: number
  glycemic_index: number
  carbohydrates: number
  protein: number
  fat: number
  fiber: number
  sugar_content: number
  sodium_content: number
  suitable_for_diabetes: number
  rating: number
  personalization_score: number
  model_used: string
  gi_category: string
  diabetes_friendly: boolean
  recommendation_reason: string
}

interface FoodCategory {
  id: string
  name: string
  icon: React.ReactNode
  color: string
  bgColor: string
  description: string
}

// Enhanced backend response interface with error property
interface FoodRecommendationResponse {
  success: boolean
  recommendations?: FoodRecommendation[]
  ml_prediction?: string
  gi_strategy?: string
  debug_info?: {
    user_seed: number
    gi_range: {
      lowest: number
      highest: number
      average: number
    }
  }
  algorithm_info?: {
    prediction_method: string
    food_selection: string
    categories: string[]
    gi_strategy_high_risk: string
    gi_strategy_low_risk: string
  }
  error?: string // Added error property
}

export default function PrediksiPageEnhanced() {
  const [formData, setFormData] = useState({
    age: "",
    glucose: "",
    insulin: "",
    bmi: "",
  })
  const [prediction, setPrediction] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [isVisible, setIsVisible] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [activeField, setActiveField] = useState<string | null>(null)
  const [animateResult, setAnimateResult] = useState(false)

  // Enhanced food recommendation states
  const [selectedCategory, setSelectedCategory] = useState<string>("")
  const [showCategorySelection, setShowCategorySelection] = useState(false)
  const [foodRecommendations, setFoodRecommendations] = useState<FoodRecommendation[]>([])
  const [loadingFood, setLoadingFood] = useState(false)
  const [foodResponseData, setFoodResponseData] = useState<FoodRecommendationResponse | null>(null)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  // Food categories
  const foodCategories: FoodCategory[] = [
    {
      id: "Buah",
      name: "Buah",
      icon: <Apple className="h-6 w-6" />,
      color: "from-red-500 to-pink-500",
      bgColor: "from-red-50 to-pink-50",
      description: "Buah-buahan segar kaya vitamin dan serat",
    },
    {
      id: "Sayur",
      name: "Sayur",
      icon: <Leaf className="h-6 w-6" />,
      color: "from-green-500 to-emerald-500",
      bgColor: "from-green-50 to-emerald-50",
      description: "Sayuran hijau dan berwarna untuk nutrisi optimal",
    },
    {
      id: "Biji-bijian",
      name: "Biji-bijian",
      icon: <Wheat className="h-6 w-6" />,
      color: "from-amber-500 to-yellow-500",
      bgColor: "from-amber-50 to-yellow-50",
      description: "Biji-bijian utuh untuk energi berkelanjutan",
    },
    {
      id: "Kacang-kacangan",
      name: "Kacang-kacangan",
      icon: <Activity className="h-6 w-6" />,
      color: "from-orange-500 to-red-500",
      bgColor: "from-orange-50 to-red-50",
      description: "Kacang dan biji untuk lemak sehat",
    },
    {
      id: "Karbohidrat",
      name: "Karbohidrat",
      icon: <Wheat className="h-6 w-6" />,
      color: "from-blue-500 to-cyan-500",
      bgColor: "from-blue-50 to-cyan-50",
      description: "Karbohidrat kompleks untuk energi stabil",
    },
    {
      id: "Protein Nabati",
      name: "Protein Nabati",
      icon: <Leaf className="h-6 w-6" />,
      color: "from-teal-500 to-green-500",
      bgColor: "from-teal-50 to-green-50",
      description: "Protein dari tumbuhan untuk kesehatan optimal",
    },
    {
      id: "Protein Hewani",
      name: "Protein Hewani",
      icon: <Beef className="h-6 w-6" />,
      color: "from-purple-500 to-pink-500",
      bgColor: "from-purple-50 to-pink-50",
      description: "Protein berkualitas tinggi dari hewan",
    },
  ]

  // Handle input change
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value,
    })
  }

  // Enhanced category selection with backend integration
  const handleCategorySelect = async (categoryId: string) => {
    setSelectedCategory(categoryId)
    setLoadingFood(true)
    setError(null)

    try {
      const numericUserData = {
        age: Number.parseFloat(formData.age),
        bmi: Number.parseFloat(formData.bmi),
        glucose: Number.parseFloat(formData.glucose),
        insulin: Number.parseFloat(formData.insulin),
      }

      console.log("Mengirim request rekomendasi makanan:", {
        category: categoryId,
        user_data: numericUserData,
      })

      const response = await fetch("http://127.0.0.1:5000/recommend_food", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          category: categoryId,
          user_data: numericUserData,
        }),
      })

      const data: FoodRecommendationResponse = await response.json()
      console.log("Response dari backend:", data)

      if (response.ok && data.success) {
        setFoodRecommendations(data.recommendations || [])
        setFoodResponseData(data)
        console.log("Berhasil mendapatkan rekomendasi:", data.recommendations)
      } else {
        console.error("Error getting food recommendations:", data)
        setError(`Gagal mendapatkan rekomendasi makanan: ${data.error || "Unknown error"}`)
        setFoodRecommendations([])
        setFoodResponseData(null)
      }
    } catch (error) {
      console.error("Failed to fetch food recommendations:", error)
      setError("Gagal terhubung ke server. Pastikan backend berjalan di http://127.0.0.1:5000")
      setFoodRecommendations([])
      setFoodResponseData(null)
    } finally {
      setLoadingFood(false)
    }
  }

  // Enhanced form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPrediction(null)
    setAnimateResult(false)
    // Reset food recommendation states
    setSelectedCategory("")
    setShowCategorySelection(false)
    setFoodRecommendations([])
    setFoodResponseData(null)

    try {
      const processingSteps = [
        "Menganalisis data kesehatan...",
        "Menghitung probabilitas risiko...",
        "Menyiapkan hasil prediksi...",
      ]

      for (let i = 0; i < processingSteps.length; i++) {
        setCurrentStep(i)
        await new Promise((resolve) => setTimeout(resolve, 500))
      }

      const numericData = {
        age: Number.parseFloat(formData.age),
        bmi: Number.parseFloat(formData.bmi),
        glucose: Number.parseFloat(formData.glucose),
        insulin: Number.parseFloat(formData.insulin),
      }

      console.log("Data yang dikirim ke backend:", numericData)

      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(numericData),
      })

      const data = await response.json()
      console.log("Response prediksi dari backend:", data)

      if (response.ok && data.success) {
        setPrediction(data.prediction === 1 ? "Risiko Tinggi" : "Risiko Rendah")
        setAnimateResult(true)

        setTimeout(() => {
          setShowCategorySelection(true)
        }, 1000)
      } else {
        setError(`Error: ${data.error || "Something went wrong"}`)
      }
    } catch (error) {
      console.error("Error during prediction:", error)
      setError("Error: Failed to fetch data from API. Pastikan backend Flask berjalan di http://127.0.0.1:5000")
    } finally {
      setLoading(false)
      setCurrentStep(0)
    }
  }

  // Helper function to get GI category styling
  const getGICategory = (gi: number) => {
    if (gi <= 35)
      return {
        label: "Sangat Rendah",
        color: "bg-green-100 text-green-800 border-green-200",
        icon: "✅",
        description: "Sangat aman untuk diabetes",
      }
    if (gi <= 50)
      return {
        label: "Rendah",
        color: "bg-blue-100 text-blue-800 border-blue-200",
        icon: "✅",
        description: "Aman untuk diabetes",
      }
    if (gi <= 70)
      return {
        label: "Sedang",
        color: "bg-yellow-100 text-yellow-800 border-yellow-200",
        icon: "⚠️",
        description: "Konsumsi terbatas",
      }
    return {
      label: "Tinggi",
      color: "bg-red-100 text-red-800 border-red-200",
      icon: "❌",
      description: "Hindari untuk diabetes",
    }
  }

  const processingSteps = [
    "Menganalisis data kesehatan...",
    "Menghitung probabilitas risiko...",
    "Menyiapkan hasil prediksi...",
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-purple-50 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-green-200 to-green-300 rounded-full opacity-20 animate-pulse"></div>
        <div
          className="absolute top-1/2 -left-20 w-60 h-60 bg-gradient-to-br from-blue-200 to-blue-300 rounded-full opacity-20 animate-bounce"
          style={{ animationDuration: "3s" }}
        ></div>
        <div
          className="absolute bottom-20 right-1/4 w-40 h-40 bg-gradient-to-br from-purple-200 to-purple-300 rounded-full opacity-20 animate-ping"
          style={{ animationDuration: "4s" }}
        ></div>
      </div>

      {/* Header */}
      <header className="bg-gradient-to-r from-green-600 via-green-700 to-green-800 text-white py-4 sticky top-0 z-50 shadow-xl">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="flex items-center group">
              <div className="relative">
                <img
                  src="/logo.png"
                  alt="DiabCare Logo"
                  className="h-12 w-auto transition-transform duration-300 group-hover:scale-110"
                />
                <div className="absolute -inset-1 bg-white rounded-full opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
              </div>
              <span className="ml-2 font-bold text-xl bg-gradient-to-r from-white to-green-100 bg-clip-text text-transparent">
                DiabCare
              </span>
            </Link>

            <nav className="hidden md:flex items-center space-x-8">
              {[
                { href: "/", label: "Beranda" },
                { href: "/fitur", label: "Fitur" },
                { href: "/statistik", label: "Statistik" },
                { href: "/testimonial", label: "Testimonial" },
                { href: "/faq", label: "FAQ" },
              ].map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="font-medium transition-all duration-300 hover:text-green-200 hover:scale-105 relative group text-green-100"
                >
                  {item.label}
                  <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-green-200 transition-all duration-300 group-hover:w-full"></span>
                </Link>
              ))}
              <Link href="/prediksi" passHref>
                <Button className="bg-white text-green-600 hover:bg-green-100 px-6 py-3 rounded-full font-medium transition-all duration-300 hover:scale-105 hover:shadow-lg">
                  <span className="flex items-center">
                    <Sparkles className="w-4 h-4 mr-2" />
                    Mulai Prediksi
                  </span>
                </Button>
              </Link>
            </nav>

            <div className="md:hidden">
              <Link href="/prediksi" passHref>
                <Button className="bg-white text-green-600 hover:bg-green-100 px-4 py-2 rounded-full font-medium transition-all duration-300 hover:scale-105">
                  Mulai Prediksi
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="container mx-auto px-4 pt-16 pb-16 relative z-10">
        <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <Link
            href="/"
            className="inline-flex items-center text-green-600 hover:text-green-700 mb-8 group transition-all duration-300"
          >
            <ArrowLeft className="mr-2 h-5 w-5 transition-transform duration-300 group-hover:-translate-x-1" />
            <span>Kembali ke Beranda</span>
          </Link>

          <div
            className={`text-center mb-12 transition-all duration-1000 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
          >
            <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-green-100 to-blue-100 rounded-full text-green-800 text-sm font-medium mb-4">
              <Calculator className="w-4 h-4 mr-2" />
              Prediksi Risiko Diabetes
            </div>
            <h1 className="text-3xl md:text-4xl font-bold mb-4">
              Prediksi Risiko{" "}
              <span className="bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                Diabetes
              </span>{" "}
              Anda
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
              Masukkan data kesehatan Anda untuk mendapatkan prediksi risiko diabetes dan rekomendasi makanan sehat
            </p>
          </div>

          <div
            className={`bg-white p-8 rounded-2xl shadow-2xl border border-gray-100 transition-all duration-1000 delay-300 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[
                  { id: "age", label: "Usia (tahun)", placeholder: "Masukkan usia Anda", icon: Activity },
                  {
                    id: "glucose",
                    label: "Kadar Glukosa (mg/dL)",
                    placeholder: "Masukkan kadar glukosa",
                    icon: TrendingUp,
                  },
                  { id: "insulin", label: "Insulin (μU/mL)", placeholder: "Masukkan kadar insulin", icon: Activity },
                  { id: "bmi", label: "BMI (kg/m²)", placeholder: "Masukkan BMI Anda", icon: Heart, step: "0.1" },
                ].map((field) => (
                  <div key={field.id} className="space-y-2 group">
                    <Label
                      htmlFor={field.id}
                      className={`text-gray-700 font-medium flex items-center transition-colors duration-300 ${activeField === field.id ? "text-green-600" : ""}`}
                    >
                      <field.icon
                        className={`w-4 h-4 mr-2 transition-colors duration-300 ${activeField === field.id ? "text-green-600" : "text-green-500"}`}
                      />
                      {field.label}
                    </Label>
                    <div className="relative">
                      <Input
                        id={field.id}
                        name={field.id}
                        type="number"
                        step={field.step}
                        placeholder={field.placeholder}
                        value={formData[field.id as keyof typeof formData]}
                        onChange={handleInputChange}
                        onFocus={() => setActiveField(field.id)}
                        onBlur={() => setActiveField(null)}
                        required
                        className={`w-full px-4 py-3 border rounded-xl transition-all duration-300 
                          ${
                            activeField === field.id
                              ? "border-green-500 ring-2 ring-green-200 shadow-md"
                              : "border-gray-300 hover:border-green-400"
                          }`}
                      />
                      {activeField === field.id && (
                        <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-green-500 animate-pulse">
                          <CheckCircle className="h-5 w-5" />
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex justify-end">
                <Button
                  type="submit"
                  className="group bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white px-8 py-4 text-lg rounded-xl disabled:opacity-50 transition-all duration-300 hover:scale-105 hover:shadow-xl transform font-medium"
                  disabled={loading}
                >
                  {loading ? (
                    <div className="flex items-center gap-3">
                      <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
                      <span>{processingSteps[currentStep]}</span>
                    </div>
                  ) : (
                    <span className="flex items-center">
                      <Sparkles className="mr-2 h-5 w-5 group-hover:animate-ping" />
                      Periksa Risiko Diabetes
                    </span>
                  )}
                </Button>
              </div>
            </form>

            {/* Error Message */}
            {error && (
              <div className="mt-8 p-6 bg-red-50 border border-red-200 rounded-xl animate-pulse">
                <div className="flex items-center">
                  <AlertTriangle className="h-6 w-6 text-red-500 mr-3" />
                  <h3 className="text-xl font-bold text-red-700">Terjadi Kesalahan</h3>
                </div>
                <p className="mt-2 text-red-600">{error}</p>
                <p className="mt-2 text-gray-600">
                  Pastikan backend Flask berjalan di http://127.0.0.1:5000 dan dapat diakses.
                </p>
              </div>
            )}

            {/* Enhanced Prediction Results */}
            {prediction && (
              <div
                className={`mt-12 space-y-8 transition-all duration-1000 ${animateResult ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}
              >
                {/* Risk Level Card with Enhanced Info */}
                <div
                  className={`p-8 rounded-2xl shadow-xl border-2 transition-all duration-500 ${
                    prediction === "Risiko Tinggi"
                      ? "bg-gradient-to-br from-red-50 to-red-100 border-red-200"
                      : "bg-gradient-to-br from-green-50 to-green-100 border-green-200"
                  }`}
                >
                  <div className="flex items-center mb-6">
                    <div
                      className={`w-12 h-12 rounded-full mr-4 flex items-center justify-center ${
                        prediction === "Risiko Tinggi" ? "bg-red-500" : "bg-green-500"
                      } ${animateResult ? "animate-bounce" : ""}`}
                      style={{ animationDuration: "1s" }}
                    >
                      {prediction === "Risiko Tinggi" ? (
                        <AlertTriangle className="h-6 w-6 text-white" />
                      ) : (
                        <CheckCircle className="h-6 w-6 text-white" />
                      )}
                    </div>
                    <div>
                      <h3
                        className={`text-2xl font-bold ${
                          prediction === "Risiko Tinggi" ? "text-red-700" : "text-green-700"
                        }`}
                      >
                        Hasil Prediksi: {prediction}
                      </h3>
                      <p className="text-gray-600">Berdasarkan Model Machine Learning</p>
                    </div>
                  </div>

                  {/* Enhanced Prediction Details */}
                  <div className="p-6 bg-white bg-opacity-60 rounded-xl">
                    <p
                      className={`text-lg ${prediction === "Risiko Tinggi" ? "text-red-600" : "text-green-600"} leading-relaxed mb-4`}
                    >
                      {prediction === "Risiko Tinggi"
                        ? "Berdasarkan data yang Anda berikan, hasil prediksi menunjukkan kemungkinan risiko diabetes Anda cukup tinggi. Disarankan untuk berkonsultasi dengan profesional kesehatan untuk evaluasi lebih lanjut."
                        : "Berdasarkan data yang Anda berikan, hasil prediksi menunjukkan risiko terkena diabetes Anda saat ini terlihat rendah. Tetap jaga gaya hidup sehat dengan pola makan yang seimbang dan rutin beraktivitas fisik."}
                    </p>

                    {/* ML Model Info */}
                    <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                      <h4 className="font-semibold text-blue-800 mb-2 flex items-center">
                        <Shield className="w-4 h-4 mr-2" />
                        Strategi Rekomendasi Makanan
                      </h4>
                      <p className="text-blue-700 text-sm">
                        {prediction === "Risiko Tinggi" &&
                          "Akan diprioritaskan makanan dengan Indeks Glikemik terendah untuk kontrol gula darah optimal"}
                        {prediction === "Risiko Rendah" &&
                          "Dapat mengonsumsi makanan dengan variasi Indeks Glikemik yang lebih fleksibel"}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Enhanced Category Selection */}
                {showCategorySelection && (
                  <div className="bg-gradient-to-br from-orange-50 to-yellow-50 p-8 rounded-2xl shadow-xl border border-orange-200">
                    <div className="flex items-center mb-6">
                      <div className="w-12 h-12 rounded-full bg-gradient-to-r from-orange-500 to-yellow-500 flex items-center justify-center mr-4">
                        <Utensils className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-orange-700">Pilih Kategori Makanan</h3>
                        <p className="text-gray-600">Pilih kategori untuk mendapatkan rekomendasi makanan</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                      {foodCategories.map((category) => (
                        <div
                          key={category.id}
                          onClick={() => handleCategorySelect(category.id)}
                          className={`p-4 rounded-xl border-2 cursor-pointer transition-all duration-300 hover:scale-105 ${
                            selectedCategory === category.id
                              ? `border-orange-400 bg-gradient-to-br ${category.bgColor} shadow-lg`
                              : "border-gray-200 bg-white hover:border-orange-300"
                          } ${loadingFood ? "pointer-events-none opacity-50" : ""}`}
                        >
                          <div className="text-center">
                            <div
                              className={`w-12 h-12 rounded-full mx-auto mb-3 flex items-center justify-center transition-all duration-300 ${
                                selectedCategory === category.id
                                  ? `bg-gradient-to-r ${category.color} text-white scale-110`
                                  : "bg-gray-100 text-gray-600"
                              }`}
                            >
                              {category.icon}
                            </div>
                            <h4 className="font-semibold text-sm text-gray-900 mb-1">{category.name}</h4>
                            <p className="text-xs text-gray-600 leading-tight">{category.description}</p>
                          </div>
                        </div>
                      ))}
                    </div>

                    {loadingFood && (
                      <div className="text-center py-4">
                        <div className="inline-flex items-center gap-2 text-orange-600">
                          <div className="animate-spin h-5 w-5 border-2 border-orange-600 border-t-transparent rounded-full" />
                          <span>Menganalisis rekomendasi makanan dengan algoritma rule-based...</span>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Enhanced Food Recommendations Display */}
                {foodRecommendations.length > 0 && foodResponseData && (
                  <div className="bg-gradient-to-br from-green-50 to-blue-50 p-8 rounded-2xl shadow-xl border border-green-200">
                    <div className="flex items-center mb-6">
                      <div className="w-12 h-12 rounded-full bg-gradient-to-r from-green-500 to-blue-500 flex items-center justify-center mr-4">
                        <Apple className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-green-700">Rekomendasi Makanan Sehat</h3>
                        <p className="text-gray-600">{foodResponseData.gi_strategy} - Dipersonalisasi untuk Anda</p>
                      </div>
                    </div>

                    {/* Algorithm Summary */}
                    <div className="bg-white bg-opacity-60 p-4 rounded-xl mb-6">
                      <div className="grid md:grid-cols-3 gap-4 text-sm">
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-blue-600" />
                          <span>
                            <strong>Prediksi ML:</strong> {foodResponseData.ml_prediction}
                          </span>
                        </div>
                        <div className="flex items-center">
                          <Shield className="w-4 h-4 mr-2 text-green-600" />
                          <span>
                            <strong>Strategi GI:</strong> {foodResponseData.gi_strategy}
                          </span>
                        </div>
                        <div className="flex items-center">
                          <Activity className="w-4 h-4 mr-2 text-purple-600" />
                          <span>
                            <strong>Rentang GI:</strong> {foodResponseData.debug_info?.gi_range.lowest}-
                            {foodResponseData.debug_info?.gi_range.highest}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Food Cards */}
                    <div className="grid md:grid-cols-1 gap-6">
                      {foodRecommendations.map((food, index) => {
                        const giCategory = getGICategory(food.glycemic_index)

                        return (
                          <div
                            key={index}
                            className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 hover:scale-[1.02] border border-green-100"
                            style={{ animationDelay: `${index * 100}ms` }}
                          >
                            {/* Header */}
                            <div className="flex items-start justify-between mb-4">
                              <div className="flex-1">
                                <h4 className="text-xl font-bold text-gray-900 mb-2">{food.name}</h4>
                                <div className="flex items-center gap-3 mb-3">
                                  <span className="px-3 py-1 bg-green-100 text-green-700 text-sm rounded-full font-medium">
                                    {food.category}
                                  </span>
                                  <span
                                    className={`px-3 py-1 text-sm rounded-full font-medium border ${giCategory.color}`}
                                  >
                                    {giCategory.icon} GI {food.glycemic_index} - {giCategory.label}
                                  </span>
                                  {food.diabetes_friendly && (
                                    <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                                      Diabetes Friendly
                                    </span>
                                  )}
                                </div>
                              </div>
                              <div className="flex items-center">
                                <Star className="w-5 h-5 text-yellow-500 fill-yellow-500 mr-1" />
                                <span className="text-lg font-bold text-gray-700">{food.rating.toFixed(1)}</span>
                              </div>
                            </div>

                            {/* Comprehensive Nutrition Grid */}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                              {/* Glycemic Index - Priority */}
                              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-3 rounded-lg text-center border border-blue-200">
                                <div className="text-2xl font-bold text-blue-700">{food.glycemic_index}</div>
                                <div className="text-xs text-blue-600 font-medium">Indeks Glikemik</div>
                                <div className="text-xs text-blue-500">{giCategory.label}</div>
                              </div>

                              {/* Calories */}
                              <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-3 rounded-lg text-center border border-orange-200">
                                <div className="text-2xl font-bold text-orange-700">{food.calories}</div>
                                <div className="text-xs text-orange-600 font-medium">Kalori</div>
                                <div className="text-xs text-orange-500">per 100g</div>
                              </div>

                              {/* Carbohydrates */}
                              <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-3 rounded-lg text-center border border-purple-200">
                                <div className="text-2xl font-bold text-purple-700">{food.carbohydrates}g</div>
                                <div className="text-xs text-purple-600 font-medium">Karbohidrat</div>
                                <div className="text-xs text-purple-500">per 100g</div>
                              </div>

                              {/* Protein */}
                              <div className="bg-gradient-to-br from-red-50 to-red-100 p-3 rounded-lg text-center border border-red-200">
                                <div className="text-2xl font-bold text-red-700">{food.protein}g</div>
                                <div className="text-xs text-red-600 font-medium">Protein</div>
                                <div className="text-xs text-red-500">per 100g</div>
                              </div>
                            </div>

                            {/* Additional Nutrients */}
                            <div className="grid grid-cols-3 gap-4 mb-4">
                              <div className="bg-gradient-to-br from-green-50 to-green-100 p-3 rounded-lg border border-green-200">
                                <div className="flex items-center justify-between">
                                  <span className="text-sm font-medium text-green-700">Serat</span>
                                  <span className="text-lg font-bold text-green-800">{food.fiber}g</span>
                                </div>
                                <div className="text-xs text-green-600">
                                  {food.fiber >= 3
                                    ? "✅ Tinggi serat"
                                    : food.fiber >= 1
                                      ? "✅ Sumber serat"
                                      : "⚠️ Rendah serat"}
                                </div>
                              </div>

                              <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-3 rounded-lg border border-yellow-200">
                                <div className="flex items-center justify-between">
                                  <span className="text-sm font-medium text-yellow-700">Lemak</span>
                                  <span className="text-lg font-bold text-yellow-800">{food.fat}g</span>
                                </div>
                                <div className="text-xs text-yellow-600">
                                  {food.fat <= 3 ? "✅ Rendah lemak" : food.fat <= 10 ? "⚠️ Sedang" : "❌ Tinggi lemak"}
                                </div>
                              </div>

                              <div className="bg-gradient-to-br from-pink-50 to-pink-100 p-3 rounded-lg border border-pink-200">
                                <div className="flex items-center justify-between">
                                  <span className="text-sm font-medium text-pink-700">Gula</span>
                                  <span className="text-lg font-bold text-pink-800">{food.sugar_content}g</span>
                                </div>
                                <div className="text-xs text-pink-600">
                                  {food.sugar_content <= 5 ? "✅ Rendah gula" : "⚠️ Perhatikan"}
                                </div>
                              </div>
                            </div>

                            {/* Diabetes Recommendation */}
                            <div className="bg-gradient-to-r from-blue-50 to-green-50 p-4 rounded-lg mb-4 border border-blue-200">
                              <h5 className="font-semibold text-gray-800 mb-2 flex items-center">
                                <Heart className="w-4 h-4 mr-2 text-red-500" />
                                Rekomendasi untuk Diabetes
                              </h5>
                              <p className="text-sm text-gray-700 mb-2">{food.recommendation_reason}</p>
                              <div className="text-sm text-gray-600">
                                <strong>Kategori GI:</strong> {giCategory.description}
                              </div>
                            </div>

                            {/* Footer */}
                            <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                              <div className="flex items-center text-green-600">
                                <Utensils className="w-4 h-4 mr-2" />
                                <span className="text-sm font-medium">Score: {food.personalization_score}</span>
                              </div>
                              <div className="flex items-center space-x-2">
                                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-green-400 to-blue-400 flex items-center justify-center">
                                  <span className="text-white text-xs font-bold">#{index + 1}</span>
                                </div>
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>

                    {/* Enhanced Tips */}
                    <div className="mt-6 p-4 bg-white bg-opacity-60 rounded-xl">
                      <h5 className="font-semibold text-green-700 mb-3 flex items-center">
                        <Info className="h-5 w-5 mr-2" />
                        Tips Konsumsi Berdasarkan Prediksi ML
                      </h5>
                      <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-700">
                        <div>
                          <h6 className="font-medium text-red-600 mb-1">🔴 Risiko Tinggi:</h6>
                          <ul className="space-y-1 text-xs">
                            <li>• Prioritaskan makanan GI terendah</li>
                            <li>• Kontrol porsi dengan ketat</li>
                            <li>• Konsultasi dengan dokter</li>
                          </ul>
                        </div>
                        <div>
                          <h6 className="font-medium text-green-600 mb-1">🟢 Risiko Rendah:</h6>
                          <ul className="space-y-1 text-xs">
                            <li>• Variasi makanan lebih fleksibel</li>
                            <li>• Tetap jaga pola makan sehat</li>
                            <li>• Rutin olahraga dan cek kesehatan</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Important Notes */}
            <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-2xl group hover:shadow-lg transition-all duration-300">
              <div className="flex items-start">
                <div className="bg-blue-100 p-2 rounded-full mr-3 group-hover:scale-110 transition-transform duration-300">
                  <Info className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-lg font-medium text-blue-800 mb-3">Catatan Penting</h3>
                  <p className="text-blue-700 leading-relaxed">
                    Hasil prediksi dan rekomendasi makanan ini hanya bersifat indikatif dan tidak menggantikan diagnosis
                    medis profesional. Selalu konsultasikan dengan dokter atau ahli gizi untuk saran medis yang tepat.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Enhanced Footer */}
      <footer className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white py-12 relative overflow-hidden mt-12">
        <div className="absolute inset-0 bg-gradient-to-r from-green-900 to-blue-900 opacity-10"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div className="group">
              <div className="flex items-center mb-4">
                <img
                  src="/logo.png"
                  alt="DiabCare Logo"
                  className="h-10 w-auto mr-2 transition-transform duration-300 group-hover:scale-110"
                />
                <span className="font-bold text-xl bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  DiabCare
                </span>
              </div>
              <p className="text-gray-400 mb-4 leading-relaxed">
                Aplikasi prediksi risiko diabetes yang dikembangkan oleh mahasiswa Sains Data Terapan PENS.
              </p>
            </div>

            {[
              {
                title: "Navigasi",
                links: [
                  { href: "/", label: "Beranda" },
                  { href: "/fitur", label: "Fitur" },
                  { href: "/statistik", label: "Statistik" },
                  { href: "/testimonial", label: "Testimonial" },
                  { href: "/faq", label: "FAQ" },
                ],
              },
              {
                title: "Fitur",
                links: [
                  { href: "/prediksi", label: "Prediksi Diabetes" },
                  { href: "/fitur", label: "Pemantauan Kesehatan" },
                  { href: "/fitur", label: "Analisis Glukosa" },
                  { href: "/fitur", label: "Evaluasi BMI" },
                  { href: "/fitur", label: "Rekomendasi Makanan Sehat" },
                ],
              },
            ].map((section, index) => (
              <div key={index}>
                <h4 className="font-bold text-lg mb-4 text-white">{section.title}</h4>
                <ul className="space-y-2">
                  {section.links.map((link, linkIndex) => (
                    <li key={linkIndex}>
                      <Link
                        href={link.href}
                        className="text-gray-400 hover:text-white transition-all duration-300 hover:translate-x-1 inline-block"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}

            <div>
              <h4 className="font-bold text-lg mb-4 text-white">Kontak</h4>
              <ul className="space-y-3">
                {[
                  { icon: "📧", text: "diabcare@gmail.com" },
                  { icon: "📱", text: "085806940713" },
                  { icon: "📍", text: "PENS, Surabaya, Indonesia" },
                ].map((contact, index) => (
                  <li
                    key={index}
                    className="flex items-center text-gray-400 hover:text-white transition-colors duration-300 group"
                  >
                    <span className="mr-3 text-lg group-hover:scale-110 transition-transform duration-300">
                      {contact.icon}
                    </span>
                    <span>{contact.text}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-700 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 mb-4 md:mb-0">© 2025 DiabCare - Aplikasi Prediksi Diabetes</p>
            <p className="text-gray-400">Dikembangkan oleh Mahasiswa Sains Data Terapan PENS</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
