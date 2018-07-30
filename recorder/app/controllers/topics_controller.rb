class TopicsController < ApplicationController
  def record
    @topic = Topic.find(params[:topic_id])
  end
end
