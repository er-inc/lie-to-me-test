Rails.application.routes.draw do
  root to: 'application#index'

  mount Sidekiq::Web, at: 'sidekiq'

  resources :topics, only: [] do
    collection do
      get :record
    end
  end

  resources :videos, only: [] do
    collection do
      post :save
    end
  end
end
